from django.urls import path
from .views import *

urlpatterns = [
    path('getAllApartments/<str:username>', getAllApartments, name='getAllApartments'),
]
