from venv import create
from django.urls import path
from .views import *

urlpatterns = [
    path('getAllServiceProviders/<str:username>', getAllServiceProviders, name='getAllServiceProviders'),
    path('getServiceProvider/<int:id>', getServiceProvider, name='getServiceProvider'),
    path('deleteServiceProvider', deleteServiceProvider, name='deleteServiceProvider'),
    path('updateServiceProvider', updateServiceProvider, name='updateServiceProvider'),
]