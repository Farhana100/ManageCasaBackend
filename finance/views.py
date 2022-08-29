from datetime import timezone
from math import floor, ceil

from django.db.models.functions import datetime
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
from serviceProvider.models import *
from django.conf import settings
from django.shortcuts import redirect
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

@api_view(['GET'])
def getFundInfo(request, username):
    building_id = Building.objects.get(user__username=username)
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
    return JsonResponse({'client_secret': intent.client_secret})

def generateDues(uid):
    try:
        user = User.objects.get(id=uid)
    except:
        return

    try:
        subs = UserSubscription.objects.filter(user=user)
    except:
        return

    for sub in subs:
        if sub.due:
            continue

        months = float(floor((datetime.datetime.now(timezone.utc) - sub.subscription_date).days / 30))
        while months - sub.package.subscription_duration > 0:
            months -= sub.package.subscription_duration


        print(sub.subscription_date)
        print(sub.package.subscription_duration)
        print("m", months)
        print()


        paid_already = False
        if sub.last_payment_date:
            paid_already = ((datetime.datetime.now(timezone.utc) - sub.last_payment_date).days <= 30)

        print("paid already", paid_already)

        if months > 0 and not paid_already:
            # create new bill
            try:
                Bill(user=user,
                     service_provider=sub.package.service_provider,
                     package=sub.package,
                     payable_amount=sub.package.fee,
                     description=sub.package.title,
                     due_date=datetime.datetime.now(timezone.utc),
                     status=False
                     ).save()
                sub.due = True
                sub.save()
            except:
                pass


@api_view(['GET'])
def getDues(request, id):
    generateDues(id)
    try:
        dues = Bill.objects.filter(user_id=id, status=False).order_by('due_date')
    except:
        to_frontend = {
            'success': False,
            'data': [],
        }
        return Response(to_frontend)

    dues = [{
        'pay_by_pk': id,
        'pay_to_pk': d.service_provider.id,
        'pay_for_pk': d.package.id,
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
                'pay_by_pk': -1,
                'pay_to_pk': -1,
                'pay_for_pk': -1,
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
def duesPayment(request, username):
    print(request.data)
    dues = request.data['dues']
    buildingId = Building.objects.get(user__username=username)

    #  DO PAYMENT HERE ------------------------------------------------>>>

    # AFTER PAYMENT ----------------------- ADDING EXPENSE

    try:
        for d in dues:
            if d['is_service_charge']:
                apartment = Apartment.objects.get(id=d['id'])
                apartment.service_charge_due_amount -= d['amount']
                apartment.paid_service_this_month = True
                apartment.save()

                # create new bill for service charge
                Bill(user=apartment.owner.user,
                     payable_amount=d['amount'],
                     description=d['description'],
                     payment_date=datetime.datetime.now(),
                     # transaction_number=...,
                     status=True
                     ).save()

                obj = Fund()
                obj.building = buildingId
                obj.owner = apartment.owner
                obj.paid_amount = d['amount']
                obj.date = datetime.datetime.now()
                obj.save()

                Building.objects.filter(user__username=username).update(total_fund=buildingId.total_fund + d['amount'])
            else:
                bill = Bill.objects.get(id=d['id'])
                bill.status = True
                bill.payment_date = datetime.datetime.now(timezone.utc)
                bill.save()

                # update subscription
                user = User.objects.get(id=d['pay_by_pk'])
                package = ServicePackage.objects.get(id=d['pay_for_pk'])
                sub = UserSubscription.objects.get(user=user, package=package)
                sub.last_payment_date = datetime.datetime.now(timezone.utc)
                sub.due = False
                sub.save()

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
