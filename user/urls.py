from django.urls import path
from .views import *

urlpatterns = [
    path('login', userLogin, name='userLogin'),
    path('getUser', getUser, name='getUser'),
    path('getAllBuildings', getAllBuildings, name='getAllBuildings'),
    path('getBuilding/<int:pk>', getBuilding, name='getBuilding'),
    path('createBuilding', createBuilding, name='createBuilding'),

    path('getAllOwners/<str:username>', getAllOwners, name='getAllOwners'),
    path('getAllTenants/<str:username>', getAllTenants, name='getAllTenants'),
    path('createOwner', createOwner, name='createOwner'),
    path('getAllApartmentsOfOwner/<str:username>', getAllApartmentsOfOwner, name='getAllApartmentsOfOwner'),
]
