from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response

import apartment
from .serializer import *
from .models import *

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def userLogin(request):
    username = request.data['username']
    password = request.data['password']
    print(username, password)
    user = authenticate(request, username=username, password=password)

    if user is not None:
        token = get_tokens_for_user(user)
        to_frontend = {
            "user_active": True,
            "username": user.username,
            "userType": "",
            "msg": "Welcome " + user.username + "!",
            "token": token,
        }
        if request.user.is_authenticated:
            try:
                print('user autheticated')
                to_frontend['userType'] = 'admin'
            except AttributeError:
                pass

        return Response(to_frontend)
    else:
        to_frontend = {
            "user_active": False,
            "username": None,
            "userType": None,
            "msg": "Invalid username or password",
            "token": None,
        }

        return Response(to_frontend)


@api_view(['GET'])
def getUser(request):
    to_frontend = {
        "user_active": request.user.is_authenticated,
        "username": str(request.user.username),
        "userType": "",
    }
    if request.user.is_authenticated:
        try:
            print(request.user.building)
            to_frontend['userType'] = 'admin'
        except AttributeError:
            pass

    test_to_frontend = {
        "user_active": True,
        "username": "Farhana100",
        "userType": "admin",
    }
    # return Response(test_to_frontend)
    return Response(to_frontend)


# --------------------------------------------------- Building admin start --------------------------------------->>>
@api_view(['GET'])
def getAllBuildings(request):
    buildings = Building.objects.all()
    serializer = BuildingSerializer(buildings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getBuilding(request, pk):
    try:
        building = Building.objects.get(id=pk)
    except Building.DoesNotExist:
        return Response(None)

    serializer = BuildingSerializer(building, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createBuilding(request):
    print("data ", request.data)
    user = request.data['user']
    building = request.data['building']

    try:
        User(username=user['username'], password=user['password'], email=user['email']).save()
    except:
        print('Error: User object could not be created 1')
        return Response(None)

    try:
        user = User.objects.get(username=user['username'])
    except User.DoesNotExist:
        print('Error: User object could not be created 2')
        return Response(None)

    building['user'] = user.id
    building = BuildingSerializer(data=building)

    if building.is_valid():
        try:
            building.save()
        except:
            print('Error: Building object could not be created 1')
            user.delete()
            return Response(None)

        return Response(building.data)

    print('Error: Building object could not be created 2')
    user.delete()
    return Response(None)


# --------------------------------------------------- Building admin end --------------------------------------->>>


# --------------------------------------------------- Owner start ---------------------------------------------->>>
@api_view(['GET'])
def getAllOwners(request, username):
    owners = Owner.objects.all().filter(apartment__building__user__username=username)
    data = []

    for owner in owners:
        data.append({

        })

    data = OwnerSerializer(owners, many=True).data
    for d in data:
        d['username'] = owners.filter(apartment__building__user_id=d['user'])

    return Response(data)


@api_view(['GET'])
def getOwner(request, pk):
    try:
        owner = Owner.objects.get(id=pk)
    except Owner.DoesNotExist:
        return Response(None)

    print(owner)
    serializer = OwnerSerializer(owner, many=False)
    return Response(serializer.data)
  

    


# --------------------------------------------------- Owner end ------------------------------------------------>>>
# --------------------------------------------------- Tenant start --------------------------------------------->>>

@api_view(['GET'])
def getAllTenants(request, username):
    tenants = Tenant.objects.all().filter(apartment__building__user__username=username)
    serializer = TenantSerializer(tenants, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTenant(request, pk):
    try:
        tenant = Tenant.objects.get(id=pk)
    except Tenant.DoesNotExist:
        return Response(None)

    print(tenant)
    serializer = TenantSerializer(tenant, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createTenant(request):
    print("data ", request.data)
    # user = request.data['user']
    # owner = request.data['owner']
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
# --------------------------------------------------- Tenant end ----------------------------------------------->>>
