from turtle import position
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from apartment.serializer import *
from user.serializer import *
from .models import *
from apartment.models import *
from user.models import *
import pytz
from django.utils import timezone

# Create your views here.

@api_view(['GET'])
def getFundInfo(request, username):
    building_id = Building.objects.get(user__username = username)
    service_charge_amount = building_id.service_charge_amount
    funds = Fund.objects.filter(building=building_id)
    print(funds)
    
    serializer = FundSerializer(funds, many=True)
    
    data = [dict(each) for each in serializer.data]
    print("data:", data)
    for each in data:
        each['payable_amount'] = service_charge_amount
        apart_no = Apartment.objects.get(owner=each['owner']).apartment_number
        each['apartment_no'] = apart_no
    
    to_frontend = {
        'funds': data,
        'total_fund': building_id.total_fund,
        'service_charge_amount': service_charge_amount
    }
        
    return Response(to_frontend)    


@api_view(['POST'])
def updateCharge(request, username):
    Building.objects.filter(user__username = username).update(service_charge_amount = request.data['service_charge'])
    
    to_frontend = {
        'success': True,
        'msg': 'updated',
    }
    
    return Response(to_frontend)