import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ContentSerializer, CourseSerializer, CourseRegistrationSerializer
from .models import Content, Course, CourseRegistration
import requests

User = get_user_model()


class CourseListCreateApiView(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              generics.GenericAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(teacher_id=user.id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CourseRetrieveUpdateDestroyApiView(mixins.RetrieveModelMixin,
                                         mixins.UpdateModelMixin,
                                         mixins.DestroyModelMixin,
                                         generics.GenericAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(teacher_id=user.id)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CourseRegistrationListCreateApiView(mixins.ListModelMixin,
                                          mixins.CreateModelMixin,
                                          generics.GenericAPIView):
    serializer_class = CourseRegistrationSerializer

    def get_queryset(self):
        user = self.request.user
        return CourseRegistration.objects.filter(student_id=user.id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CourseRegistrationRetrieveUpdateDestroyApiView(mixins.RetrieveModelMixin,
                                                     mixins.UpdateModelMixin,
                                                     mixins.DestroyModelMixin,
                                                     generics.GenericAPIView):
    serializer_class = CourseRegistrationSerializer

    def get_queryset(self):
        user = self.request.user
        return CourseRegistration.objects.filter(student_id=user.id)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AllCoursesListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', ]


class ContentCreateApiView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self):
        course_id = self.request.data.get('course_id')
        return Content.objects.filter(course__teacher_id=self.request.user.id, course_id=course_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ContentRetrieveUpdateDestroy(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                                   generics.GenericAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self):
        return Content.objects.filter(course__teacher_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


def paypal_token():
    p_client_id = settings.PAYPAL_CLIENT_ID
    p_client_secret = settings.PAYPAL_CLIENT_SECRET
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = {
        "client_id": p_client_id,
        "client_secret": p_client_secret,
        "grant_type": "client_credentials"
    }
    headers = {"content-type": "application/x-www-form-urlencoded",
               "Authorization": 'Basic {0}'.format(
                   base64.b64encode(f"{p_client_id}:{p_client_secret}".encode()).decode())}

    return requests.post(url, data, headers=headers).json()


class CourseBuyApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        course_reg = CourseRegistration.objects.filter(student=request.user.id, paid=True)
        serializer = CourseRegistrationSerializer(course_reg, many=True)
        return Response(serializer.data)

    def post(self, request):
        course_id = request.data.get('course')
        student_id = request.data.get('student')
        course = Course.objects.get(id=course_id)
        student = User.objects.get(id=student_id)
        course_registration = CourseRegistration.objects.create(
            course=course,
            student=student
        )
        request.session['crid'] = course_registration.pk
        headers = {
            'Authorization': f'Bearer {paypal_token()["access_token"]}',
        }
        json_data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "items": [
                        {
                            "name": course.title,
                            "description": course.title,
                            "quantity": "1",
                            "unit_amount": {
                                "currency_code": "USD",
                                "value": course.price
                            }
                        }
                    ],
                    "amount": {
                        "currency_code": "USD",
                        "value": course.price,
                        "breakdown": {
                            "item_total": {
                                "currency_code": "USD",
                                "value": course.price
                            }
                        }
                    }
                }
            ],
            "application_context": {
                "return_url": f"https://127.0.0.1:8000/api/oc/return/{course_registration.pk}",
                "cancel_url": f"https://127.0.0.1:8000/api/oc/cancel/{course_registration.pk}"
            }
        }
        response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers,
                                 json=json_data).json()
        return Response(response)


def paypal_return(request, pk):
    token = request.GET.get('token')
    payer_id = request.GET.get('PayerID')
    course_registration = CourseRegistration.objects.get(id=pk)
    course_registration.paid = True
    course_registration.paypal_payment_id = payer_id
    course_registration.save()
    return HttpResponse(f'payment success - token={token} and payerID={payer_id}')


def paypal_cancel(request, pk):
    course_registration = CourseRegistration.objects.get(id=pk)
    course_registration.delete()
    return HttpResponse('payment failed')
