from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CourseSerializer, CourseRegistrationSerializer
from .models import Course, CourseRegistration


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


class CourseRetriveUpdateDestroyApiView(mixins.RetrieveModelMixin,
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


class CourseRegistrationRetriveUPdateDestroyApiView(mixins.RetrieveModelMixin,
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
    permission_classes = (AllowAny,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
