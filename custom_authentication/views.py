from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import TeacherSerializer, StudentSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class TeacherCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (AllowAny,)

class StudentCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)