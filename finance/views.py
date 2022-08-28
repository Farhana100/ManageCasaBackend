from http import client
from turtle import position
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from ManageCasa.settings import CORS_ORIGIN_WHITELIST
from .serializer import *
from apartment.serializer import *
from user.serializer import *
from .models import *
from apartment.models import *
from user.models import *
from django.conf import settings
from django.shortcuts import redirect
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

@api_view(['GET'])
def getFundInfo(request, username):
    building_id = Building.objects.get(user__username = username)
    service_charge_amount = building_id.service_charge_amount
    funds = Fund.objects.filter(building=building_id)
    
    
    serializer = FundSerializer(funds, many=True)
    
    data = [dict(each) for each in serializer.data]
    
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


@api_view(['GET'])
def getExpenseInfo(request, username):
    building_id = Building.objects.get(user__username = username)
    
    funds = Expense.objects.filter(building=building_id)
    print(funds)
    
    serializer = ExpenseSerializer(funds, many=True)
    data = [dict(each) for each in serializer.data]
    to_frontend = {
        'expenses': data,
        'total_fund': building_id.total_fund
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

@api_view(['POST'])
def addExpense(request, username):
    print("ashlo data:", request.data)
    buildingId = Building.objects.get(user__username = username)
    obj = Expense()
    obj.building = buildingId
    obj.date = request.data['date']
    obj.category = request.data['purpose']
    obj.paid_amount = request.data['amount']
    obj.comment = request.data['comment']
    obj.save()
    
    Building.objects.filter(user__username = username).update(total_fund = buildingId.total_fund - float(request.data['amount']))
    
    to_frontend = {
        'success': True,
        'msg': 'added',
    }
    
    return Response(to_frontend)


@api_view(['POST'])
def stripeCheckoutSession(request):
    amount = request.data['amount']
    
    intent = stripe.PaymentIntent.create(
    amount=amount,
    currency="usd",
    automatic_payment_methods={"enabled": True},
    )
    
    to_frontend = {
        'client_secret': intent.client_secret,
        'success': True,
    }
    
 
    print("checkout")
    print(intent.client_secret)
    return JsonResponse({'client_secret':intent.client_secret})


