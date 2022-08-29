from django.urls import path
from .views import *

urlpatterns = [
    path('login', userLogin, name='userLogin'),
    path('register', userRegister, name='userRegister'),
    path('getUser', getUser, name='getUser'),
    path('getBasics/<str:username>', getBasics, name='getBasics'),

    path('getAllBuildings', getAllBuildings, name='getAllBuildings'),
    path('getBuilding/<int:pk>', getBuilding, name='getBuilding'),
    path('createBuilding', createBuilding, name='createBuilding'),

    path('getAllOwners/<str:username>', getAllOwners, name='getAllOwners'),
    path('getAllTenants/<str:username>', getAllTenants, name='getAllTenants'),
    path('createOwner', createOwner, name='createOwner'),
    path('deleteOwner', deleteOwner, name='deleteOwner'),
    path('createTenant', createTenant, name='createTenant'),
    path('deleteTenant', deleteTenant, name='deleteTenant'),
    path('getAllApartmentsOfOwner/<str:username>', getAllApartmentsOfOwner, name='getAllApartmentsOfOwner'),
]
