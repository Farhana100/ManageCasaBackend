from turtle import position

from django.db.models.functions import datetime
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
    building_id = Building.objects.get(user__username=username)
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


@api_view(['GET'])
def getExpenseInfo(request, username):
    building_id = Building.objects.get(user__username=username)

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
    Building.objects.filter(user__username=username).update(service_charge_amount=request.data['service_charge'])

    to_frontend = {
        'success': True,
        'msg': 'updated',
    }

    return Response(to_frontend)


@api_view(['POST'])
def addExpense(request, username):
    print("ashlo data:", request.data)
    buildingId = Building.objects.get(user__username=username)
    obj = Expense()
    obj.building = buildingId
    obj.date = request.data['date']
    obj.category = request.data['purpose']
    obj.paid_amount = request.data['amount']
    obj.comment = request.data['comment']
    obj.save()

    Building.objects.filter(user__username=username).update(
        total_fund=buildingId.total_fund - float(request.data['amount']))

    to_frontend = {
        'success': True,
        'msg': 'added',
    }

    return Response(to_frontend)


@api_view(['GET'])
def getDues(request, id):
    try:
        dues = Bill.objects.filter(user_id=id, status=False).order_by('due_date')
    except:
        to_frontend = {
            'success': False,
            'data': [],
        }
        return Response(to_frontend)

    dues = [{
        'pay_to': d.service_provider.company_name,
        'due_date': d.due_date.date(),
        'description': d.description,
        'amount': d.payable_amount,
        'id': d.id,
        'is_service_charge': False,
        'selected': False
    } for d in dues]

    # add service charge
    try:
        owner = Owner.objects.get(user_id=id)
        apartment = Apartment.objects.get(owner=owner)
        if apartment.service_charge_due_amount != 0:
            dues.append({
                'pay_to': "Building Fund",
                'due_date': '',
                'description': 'Service Charge',
                'amount': apartment.service_charge_due_amount,
                'id': apartment.id,  # if service charge then apartment id
                'is_service_charge': True,
                'selected': False
            })
    except:
        pass

    to_frontend = {
        'success': True,
        'data': dues,
    }

    return Response(to_frontend)


@api_view(['POST'])
def duesPayment(request):
    print(request.data)
    dues = request.data['dues']

    #  DO PAYMENT HERE ------------------------------------------------>>>

    # AFTER PAYMENT ----------------------- ADDING EXPENSE

    try:
        for d in dues:
            if d['is_service_charge']:
                apartment = Apartment.objects.get(id=d['id'])
                apartment.service_charge_due_amount -= d['amount']
                apartment.save()

                # create new bill for service charge
                Bill(user=apartment.owner.user,
                     payable_amount=d['amount'],
                     description=d['description'],
                     payment_date=datetime.datetime.now(),
                     # transaction_number=...,
                     status=True
                     ).save()
            else:
                bill = Bill.objects.get(id=d['id'])
                bill.status = True
                bill.payment_date = datetime.datetime.now()
                bill.save()

        to_frontend = {
            'success': True,
            'msg': 'successful',
        }

        return Response(to_frontend)
    except:
        to_frontend = {
            'success': False,
            'msg': 'smth is wrond idk',
        }

        return Response(to_frontend)


@api_view(['GET'])
def getPayments(request, id):
    try:
        payments = Bill.objects.filter(user_id=id, status=True).order_by('due_date')
    except:
        to_frontend = {
            'success': False,
            'data': [],
        }
        return Response(to_frontend)

    payments = [{
        'pay_to': d.service_provider.company_name if d.service_provider else "Building Fund",
        'due_date': d.due_date.date(),
        'payment_date': d.payment_date.date(),
        'description': d.description,
        'amount': d.payable_amount,
        'transaction_id': d.transaction_number,
        # 'id': d.id,
        # 'is_service_charge': False,
        # 'selected': False
    } for d in payments]

    to_frontend = {
        'success': True,
        'data': payments,
    }

    return Response(to_frontend)