from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *


# Create your views here.

@api_view(['GET'])
def getAllServiceProviders(request, username):
    print("all service providers of ", username)
    to_frontend = {
        'success': True,
        'data': []
    }
    return Response(to_frontend)

@api_view(['GET'])
def getServiceProvider(request, id):
    print("get service provider ", id)
    to_frontend = {
        'success': True,
        'data': []
    }
    return Response(to_frontend)

@api_view(['POST'])
def deleteServiceProvider(request):
    id = request.data['serviceProvider_pk']
    print("get service provider ", id)
    to_frontend = {
        'success': True,
        'data': []
    }
    return Response(to_frontend)

@api_view(['POST'])
def updateServiceProvider(request):
    id = request.data['serviceProvider_pk']
    print("get service provider ", id)
    to_frontend = {
        'success': True,
        'data': []
    }
    return Response(to_frontend)
