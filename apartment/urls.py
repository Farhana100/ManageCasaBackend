from django.urls import path
from .views import *

urlpatterns = [
    path('createApartment', createApartment, name='createApartment'),
    path('getAllApartments/<str:username>', getAllApartments, name='getAllApartments'),
    path('getApartment/<int:pk>', getApartment, name='getApartment'),
]
