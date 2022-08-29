from datetime import timezone

from django.db.models.functions import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *


# packages:
# service_provider
# title
# description
# fee
# subscription_duration

# service provider
# building
# company_name
# address
# image
# phone_number
# bkash_acc_number
# details
# website

@api_view(['POST'])
def createServiceProvider(request):
    print(request.data)
    # service provider
    building = request.data['building']
    company_name = request.data['company_name']
    address = request.data['address']
    image = request.data['image']
    phone_number = request.data['phone_number']
    bkash_acc_number = request.data['bkash_acc_number']
    details = request.data['details']
    website = request.data['website']

    print(image)

    to_frontend = {
        "msg": "test",
        "success": False,
    }
    # return Response(to_frontend)

    try:
        building = Building.objects.get(user__username=building)
    except:
        print("building not found")
        to_frontend['msg'] = "building not found"
        return Response(to_frontend)

    try:
        ServiceProvider(building=building,
                        company_name=company_name,
                        address=address,
                        image=image,
                        phone_number=phone_number,
                        bkash_acc_number=bkash_acc_number,
                        details=details,
                        website=website).save()
    except:
        print("Service Provider creation failed")
        to_frontend['msg'] = "Service Provider creation failed"
        return Response(to_frontend)

    to_frontend['msg'] = "Service Provider created"
    to_frontend['success'] = True
    print("Service Provider created")
    return Response(to_frontend)


@api_view(['GET'])
def getAllServiceProviders(request, username):
    print("all service providers of ", username)

    try:
        serviceProviders = ServiceProvider.objects.filter(building__user__username=username)
    except:
        print("building not found: ", username)
        to_frontend = {
            'success': True,
            'data': []
        }
        return Response(to_frontend)

    data = []

    for serviceProvider in serviceProviders:
        print(serviceProvider)
        data.append({
            'id': serviceProvider.id,
            'company_name': serviceProvider.company_name,
            'address': serviceProvider.address,
            'image': serviceProvider.get_image(),
            'phone_number': serviceProvider.phone_number,
            'bkash_acc_number': serviceProvider.bkash_acc_number,
            'details': serviceProvider.details,
        })

    to_frontend = {
        "data": data,
        "msg": "datafetched",
        "success": True,
    }

    return Response(to_frontend)


@api_view(['GET'])
def getServiceProvider(request, id, uid):
    print("get service provider ", id)
    try:
        serviceP = ServiceProvider.objects.get(id=id)
    except:
        to_frontend = {
            'success': False
        }
        return Response(to_frontend)

    try:
        packages = ServicePackage.objects.filter(service_provider=serviceP).order_by('fee')
    except:
        print('smth is wrong')
        to_frontend = {
            'success': False,
            'msg': 'smth is wrong in the backend'
        }
        return Response(to_frontend)

    # packages:
    # service_provider
    # title
    # description
    # fee
    # subscription_duration

    packages = [{
        'package_id': p.id,
        'title': p.title,
        'description': p.description,
        'fee': p.fee,
        'duration': p.subscription_duration,
        'subscribed': UserSubscription.objects.filter(user_id=uid, package_id=p.id).exists()
    } for p in packages]

    to_frontend = {
        'success': True,
        'id': serviceP.id,
        'company_name': serviceP.company_name,
        'address': serviceP.address,
        'image': serviceP.get_image(),
        'phone_number': serviceP.phone_number,
        'bkash_acc_number': serviceP.bkash_acc_number,
        'details': serviceP.details,
        'website': serviceP.website,
        'packages': packages

    }
    return Response(to_frontend)


@api_view(['POST'])
def deleteServiceProvider(request):
    id = request.data['pk']
    print("get service provider ", id)

    to_frontend = {
        'success': True
    }

    try:
        ServiceProvider.objects.get(id=id).delete()
    except:
        to_frontend['success'] = False
        to_frontend['msg'] = "smths wrong"

    return Response(to_frontend)


@api_view(['POST'])
def editServiceProvider(request):
    print(request.data)
    # service provider
    building = request.data['building']
    pk = request.data['pk']
    company_name = request.data['company_name']
    address = request.data['address']
    image = request.data['image']
    phone_number = request.data['phone_number']
    bkash_acc_number = request.data['bkash_acc_number']
    details = request.data['details']
    website = request.data['website']

    to_frontend = {
        "msg": "test",
        "success": False,
    }
    # return Response(to_frontend)

    try:
        serviceP = ServiceProvider.objects.get(id=pk)
    except:
        print("Service provider not found")
        to_frontend['msg'] = "Service provider not found"
        return Response(to_frontend)
    try:
        serviceP.company_name = company_name
        serviceP.address = address
        serviceP.phone_number = phone_number
        serviceP.bkash_acc_number = bkash_acc_number
        serviceP.details = details
        serviceP.website = website

        if image:
            serviceP.image = image
        serviceP.save()

    except:
        print("Service Provider update failed")
        to_frontend['msg'] = "Service Provider update failed"
        return Response(to_frontend)

    to_frontend['msg'] = "Service Provider updated"
    to_frontend['success'] = True
    print("Service Provider updated")
    return Response(to_frontend)


@api_view(['POST'])
def createServicePackage(request):
    print(request.data)
    id = request.data['serviceProvider_pk']
    title = request.data['title']
    description = request.data['description']
    fee = request.data['fee']
    subscription_duration = request.data['subscription_duration']

    to_frontend = {
        'success': False,
        'msg': 'test',
    }

    try:
        serviceP = ServiceProvider.objects.get(id=id)
    except:
        print('Error: ', 'service provider not found')
        to_frontend['msg'] = 'service provider not found'
        return Response(to_frontend)

    try:
        ServicePackage(service_provider=serviceP, title=title, description=description, fee=fee,
                       subscription_duration=subscription_duration).save()
    except:
        print('Error: ', 'package could not be created')
        to_frontend['msg'] = 'package could not be created'
        return Response(to_frontend)

    to_frontend['success'] = True
    to_frontend['msg'] = 'package created'
    return Response(to_frontend)


@api_view(['POST'])
def editServicePackage(request):
    print(request.data)
    id = request.data['pk']
    title = request.data['title']
    description = request.data['description']
    fee = request.data['fee']
    subscription_duration = request.data['subscription_duration']

    to_frontend = {
        'success': False,
        'msg': 'test',
    }

    try:
        package = ServicePackage.objects.get(id=id)
    except:
        print('Error: ', 'package not found')
        to_frontend['msg'] = 'package not found'
        return Response(to_frontend)

    try:
        package.title = title
        package.description = description
        package.fee = fee
        package.subscription_duration = subscription_duration
        package.save()
    except:
        print('Error: ', 'package could not be updated')
        to_frontend['msg'] = 'package could not be updated'
        return Response(to_frontend)

    to_frontend['success'] = True
    to_frontend['msg'] = 'package updated'
    return Response(to_frontend)


@api_view(['POST'])
def deleteServicePackage(request):
    pk = request.data['pk']
    print(request.data)

    to_frontend = {
        'success': False,
        'msg': 'test',
    }

    try:
        ServicePackage.objects.get(id=pk).delete()
    except:
        print('Error: package not deleted')
        to_frontend['msg'] = 'package not deleted'
        return Response(to_frontend)

    to_frontend['success'] = True
    return Response(to_frontend)


@api_view(['POST'])
def subscribePackage(request):
    package_pk = request.data['package_pk']
    user_pk = request.data['user_pk']
    print(request.data)

    to_frontend = {
        'success': False,
        'msg': 'test',
    }

    try:
        package = ServicePackage.objects.get(id=package_pk)
    except:
        print('Error: package not found')
        to_frontend['msg'] = 'package not found'
        return Response(to_frontend)

    try:
        user = User.objects.get(id=user_pk)
    except:
        print('Error: user not found')
        to_frontend['msg'] = 'user not found'
        return Response(to_frontend)

    try:
        UserSubscription(user=user, package=package, subscription_date=datetime.datetime.now(timezone.utc)).save()
    except:
        print('Error: subscription failed')
        to_frontend['msg'] = 'subscription failed'
        return Response(to_frontend)

    to_frontend['success'] = True
    return Response(to_frontend)


@api_view(['POST'])
def unsubscribePackage(request):
    package_pk = request.data['package_pk']
    user_pk = request.data['user_pk']
    print(request.data)

    to_frontend = {
        'success': False,
        'msg': 'test',
    }

    try:
        package = ServicePackage.objects.get(id=package_pk)
    except:
        print('Error: package not found')
        to_frontend['msg'] = 'package not found'
        return Response(to_frontend)

    try:
        user = User.objects.get(id=user_pk)
    except:
        print('Error: user not found')
        to_frontend['msg'] = 'user not found'
        return Response(to_frontend)

    try:
        UserSubscription.objects.get(user=user, package=package).delete()
    except:
        print('Error: subscription failed')
        to_frontend['msg'] = 'subscription failed'
        return Response(to_frontend)

    to_frontend['success'] = True
    return Response(to_frontend)


@api_view(['GET'])
def getServicePackage(request, id):
    # packages:
    # service_provider
    # title
    # description
    # fee
    # subscription_duration

    try:
        package = ServicePackage.objects.get(id=id)
    except:
        to_frontend = {
            'success': False,
            'msg': "package not found"
        }
        print('package not found')
        return Response(to_frontend)

    to_frontend = {
        'success': True,
        'package_id': package.id,
        'title': package.title,
        'description': package.description,
        'fee': package.fee,
        'duration': package.subscription_duration
    }
    return Response(to_frontend)
