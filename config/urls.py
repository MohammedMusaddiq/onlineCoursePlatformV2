from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/u/', include('custom_authentication.urls', namespace='user')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/oc/',
         include('online_course.urls', namespace='online_course')),
]
