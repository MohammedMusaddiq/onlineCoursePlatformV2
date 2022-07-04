from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('register/t/', views.TeacherCreateAPIView.as_view()),
    path('register/s/', views.StudentCreateAPIView.as_view()),
    path('verify-otp/', views.VerifyOtp.as_view()),
]
