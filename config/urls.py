from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('custom_authentication.urls', namespace='user')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/online-course/',
         include('online_course.urls', namespace='online_course')),
]
