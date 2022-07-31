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
    try:
        apartment = Apartment.objects.get(id=pk)
    except Apartment.DoesNotExist:
        return Response(None)

    print(apartment)
    serializer = ApartmentSerializer(apartment, many=False)
    return Response(serializer.data)


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