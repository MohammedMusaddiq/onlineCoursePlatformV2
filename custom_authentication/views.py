import datetime
import requests
from django.conf import settings
from oauth2_provider.models import Application, RefreshToken, AccessToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from .serializers import TeacherSerializer, StudentSerializer
from django.contrib.auth import get_user_model
from .email import send_otp_via_mail

User = get_user_model()


def delete_revoked_tokens():
    rtokens = RefreshToken.objects.all()
    for r in rtokens:
        if r.revoked:
            r.delete()


def create_application(request):
    if user := User.objects.get(id=1):
        application = Application.objects.filter(user=user)
        if application:
            application = Application.objects.all()[0]
        else:
            application = Application.objects.create(user=user, name='dot-app', client_type='public',
                                                     authorization_grant_type='password', )
        return {'client_id': application.client_id, }


class LoginApiView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        delete_revoked_tokens()
        username = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        data = create_application(request)
        time_delta = datetime.datetime.now()
        if token_obj := AccessToken.objects.filter(user=user, expires__gt=time_delta).first():
            token = token_obj.token
            data = {"token": token, "user_id": user.id}
            return Response(data)
        else:
            if token_obj := AccessToken.objects.filter(user=user, expires__lte=datetime.datetime.now()).first():
                refresh_token = RefreshToken.objects.get(access_token_id=token_obj.id)
                payload = {'grant_type': 'refresh_token', 'refresh_token': refresh_token.token,
                           'client_id': data['client_id'], }
                response = requests.post("http://localhost:8000/o/token/", data=payload).json()
                response['user_id'] = user.id
                return Response(response)
            payload = {'client_id': data['client_id'], 'username': username, 'password': password,
                       'grant_type': 'password', }
            response = requests.post("http://localhost:8000/o/token/", data=payload).json()
            response['user_id'] = user.id

            return Response(response)


class TeacherCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        s = serializer.save()
        send_otp_via_mail(s.email)


class StudentCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        sz = serializer.save()
        send_otp_via_mail(sz.email)


class VerifyOtp(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = User.objects.filter(email=email).first()
        if int(user.otp) == int(otp):
            user.is_verified = True
            user.save()
            data = {'message': "OTP Verification Successful"}
            return Response(data)
        return Response({"message": "Wrong OTP Entered"})
