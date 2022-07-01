from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('register/teacher/', views.TeacherCreateAPIView.as_view()),
    path('register/student/', views.StudentCreateAPIView.as_view()),
]
