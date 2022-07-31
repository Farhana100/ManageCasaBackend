from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('user.urls')),
    path('', include('apartment.urls')),
    path('admin/', admin.site.urls),
]
