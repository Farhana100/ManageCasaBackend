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
def updateServiceProvider(request):
    id = request.data['serviceProvider_pk']
    print("get service provider ", id)
    to_frontend = {
        'success': True,
        'data': []
    }
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
        return  Response(to_frontend)

    try:
        ServicePackage(service_provider=serviceP, title=title, description=description, fee=fee, subscription_duration=subscription_duration).save()
    except:
        print('Error: ', 'package could not be created')
        to_frontend['msg'] = 'package could not be created'
        return Response(to_frontend)

    to_frontend['success'] = True
    to_frontend['msg'] = 'package created'
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
        package = ServicePackage.objects.get(id=pk).delete()
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
        UserSubscription(user=user, package=package).save()
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


