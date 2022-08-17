from django.contrib.auth import login, logout, authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializer import *
from .models import *

# --------------------------------------------------- Building admin start --------------------------------------->>>
@api_view(['GET'])
def getAllApartments(request, username):
    apartments = Apartment.objects.all().filter(building__user__username=username)
    serializer = ApartmentSerializer(apartments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getApartment(request, pk):

    to_frontend = {
        "none": True,
    }
    print(type(pk))
    try:
        apartment = Apartment.objects.get(id=pk)
    except Apartment.DoesNotExist:
        print("why are you here?")
        return Response(to_frontend)

    to_frontend['apartment_pk'] = apartment.pk
    print(apartment.pk)
    to_frontend['apartment_floor_number'] = apartment.floor_number
    print(apartment.floor_number)
    to_frontend['apartment_number'] = apartment.apartment_number
    print(apartment.apartment_number)
    to_frontend['apartment_building_address'] = apartment.building.address
    print(apartment.building.address)
    print()
    to_frontend['apartment_owner'] = apartment.owner
    if apartment.owner:
        to_frontend['apartment_owner'] = apartment.owner.pk
        to_frontend['owner_name'] = apartment.owner.user.first_name + ' ' + apartment.owner.user.last_name
        to_frontend['owner_bkash_acc_number'] = apartment.owner.bkash_acc_number
        to_frontend['owner_phone_number'] = apartment.owner.phone_number
        to_frontend['owner_image'] = apartment.owner.get_image()

    print(apartment.owner)
    print()
    to_frontend['apartment_tenant'] = apartment.tenant
    if apartment.tenant:
        to_frontend['apartment_tenant'] = apartment.tenant.pk
        to_frontend['tenant_name'] = apartment.tenant.user.first_name + ' ' + apartment.tenant.user.last_name
        to_frontend['tenant_bkash_acc_number'] = apartment.tenant.bkash_acc_number
        to_frontend['tenant_phone_number'] = apartment.tenant.phone_number
        to_frontend['tenant_arrival_date'] = apartment.tenant.arrival_date
        to_frontend['tenant_departure_date'] = apartment.tenant.departure_date
        to_frontend['tenant_image'] = apartment.tenant.get_image()

    print(apartment.tenant)
    to_frontend['apartment_rent'] = apartment.rent
    print(apartment.rent)

    apartment = ApartmentSerializer(apartment, many=False).data

    print("here-------")
    print(to_frontend)
    # to_frontend['apartment'] = apartment
    to_frontend['none'] = False

    return Response(to_frontend)


@api_view(['POST'])
def createapartment(request):
    # print("data ", request.data)
    # user = request.data['user']
    # building = request.data['building']
    #
    # try:
    #     User(username=user['username'], password=user['password'], email=user['email']).save()
    # except:
    #     print('Error: User object could not be created 1')
    #     return Response(None)
    #
    # try:
    #     user = User.objects.get(username=user['username'])
    # except User.DoesNotExist:
    #     print('Error: User object could not be created 2')
    #     return Response(None)
    #
    # building['user'] = user.id
    # building = BuildingSerializer(data=building)
    #
    # if building.is_valid():
    #     try:
    #         building.save()
    #     except:
    #         print('Error: Building object could not be created 1')
    #         user.delete()
    #         return Response(None)
    #
    #     return Response(building.data)
    #
    # print('Error: Building object could not be created 2')
    # user.delete()
    return Response(None)

# --------------------------------------------------- Building admin end --------------------------------------->>>