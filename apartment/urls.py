from django.urls import path
from .views import *

urlpatterns = [
    path('createApartment', createApartment, name='createApartment'),
    path('updateApartment', updateApartment, name='updateApartment'),
    path('deleteApartment', deleteApartment, name='deleteApartment'),
    path('getAllApartmentsWithoutOwners/<str:username>', getAllApartmentsWithoutOwners, name='getAllApartmentsWithoutOwners'),
    path('getAllApartmentsWithoutTenants/<str:username>', getAllApartmentsWithoutTenants, name='getAllApartmentsWithoutTenants'),
    path('getAllApartments/<str:username>', getAllApartments, name='getAllApartments'),
    path('getApartment/<int:pk>', getApartment, name='getApartment'),
]
