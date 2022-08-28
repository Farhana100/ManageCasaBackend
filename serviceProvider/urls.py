from venv import create
from django.urls import path
from .views import *

urlpatterns = [
    path('getAllServiceProviders/<str:username>', getAllServiceProviders, name='getAllServiceProviders'),
    path('getServiceProvider/<int:id>/<int:uid>', getServiceProvider, name='getServiceProvider'),
    path('getServicePackage/<int:id>', getServicePackage, name='getServicePackage'),
    path('createServiceProvider', createServiceProvider, name='createServiceProvider'),
    path('deleteServiceProvider', deleteServiceProvider, name='deleteServiceProvider'),
    path('editServiceProvider', editServiceProvider, name='editServiceProvider'),
    path('editServicePackage', editServicePackage, name='editServicePackage'),
    path('createServicePackage', createServicePackage, name='createServicePackage'),
    path('deleteServicePackage', deleteServicePackage, name='deleteServicePackage'),
    path('subscribePackage', subscribePackage, name='subscribePackage'),
    path('unsubscribePackage', unsubscribePackage, name='unsubscribePackage'),
]