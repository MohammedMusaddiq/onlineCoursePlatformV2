from django.urls import path
from . import views

app_name = 'online_course'

urlpatterns = [
    path('courses/', views.CourseListCreateApiView.as_view()),
    path('courses/<pk>/', views.CourseRetriveUpdateDestroyApiView.as_view()),
    path('course-registeration/',
         views.CourseRegistrationListCreateApiView.as_view()),
    path('course-registeration/<pk>/',
         views.CourseRegistrationRetriveUPdateDestroyApiView.as_view()),
    path('course/', views.AllCoursesListApiView.as_view()),

]