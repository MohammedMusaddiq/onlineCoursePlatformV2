from django.urls import path
from . import views

app_name = 'online_course'

urlpatterns = [
    path('courses/', views.CourseListCreateApiView.as_view()),
    path('courses/<pk>/', views.CourseRetrieveUpdateDestroyApiView.as_view()),

    path('content/', views.ContentCreateApiView.as_view()),
    path('content/<pk>/', views.ContentRetrieveUpdateDestroy.as_view()),

    # path('course-registeration/',
    #      views.CourseRegistrationListCreateApiView.as_view()),
    path('course-registeration/',
         views.CourseBuyApiView.as_view()),
    path('course-registeration/<pk>/',
         views.CourseRegistrationRetrieveUpdateDestroyApiView.as_view()),

    path('s/course/', views.AllCoursesListApiView.as_view()),

    path('return/<int:pk>/', views.paypal_return, name='paypal return'),
    path('cancel/<int:pk>/', views.paypal_cancel, name='paypal cancel'),

]
