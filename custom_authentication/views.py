import datetime
import requests
from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import TeacherSerializer, StudentSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginApiView(APIView):
    def post(self, request, format=None):
        email = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            client_id = settings.CLIENT_ID
            client_secret = settings.CLIENT_SECRET
            data = {
                'grant_type': 'password',
                'username': email,
                'password': password,
                'client_id': client_id,
                'client_secret': client_secret,
            }
            response = requests.post(
                'http://localhost:8000/o/token/', data=data)
            token = response.json()['access_token']
            return Response({'success': True, 'Token': token})
        return Response({'success': False})


class TeacherCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (AllowAny,)


class StudentCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)
