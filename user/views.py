from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from apartment.serializer import *
from .models import *
from apartment.models import *

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
            "uid": user.id,
            "userType": None,
            "msg": "Welcome " + user.username + "!",
            "token": token,
            "building": '',
        }
        print('here')
        try:
            user.building
            to_frontend['userType'] = 'admin'
            to_frontend['building'] = user.username
        except AttributeError:
            try:
                user.owner
                to_frontend['userType'] = 'owner'
                to_frontend['building'] = Apartment.objects.filter(owner=user.owner)[0].building.user.username
            except AttributeError:
                try:
                    user.tenant
                    to_frontend['userType'] = 'tenant'
                    to_frontend['building'] = Apartment.objects.filter(tenant=user.tenant)[0].building.user.username
                except AttributeError:
                    to_frontend['userType'] = None

        print(to_frontend)

        return Response(to_frontend)
    else:
        to_frontend = {
            "user_active": False,
            "username": None,
            "uid": -1,
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
def userRegister(request):
    # user
    # address
    # phone_number
    # num_of_apartments
    # num_of_tenants
    # service_charge_amount
    # total_fund

    print("data ", request.data)
    address = request.data['address']
    username = request.data['username']
    lastname = request.data['lastname']
    firstname = request.data['firstname']
    password = make_password(request.data['password'])
    email = request.data['email']
    phone_number = request.data['phone_number']
    bkash_acc_number = request.data['bkash_acc_number']

    to_frontend = {
        "user_active": False,
    }

    # return Response(to_frontend)

    try:
        User(username=username, password=password, first_name=firstname, last_name=lastname, email=email).save()
        user = User.objects.get(username=username)
    except:
        print('user could not be created')
        to_frontend['msg'] = 'user could not be created'
        return Response(to_frontend)

    try:
        Building(user=user, address=address, phone_number=phone_number, bkash_acc_number=bkash_acc_number).save()
    except:
        user.delete()
        print('building could not be created')
        to_frontend['msg'] = 'building could not be created'
        return Response(to_frontend)

    token = get_tokens_for_user(user)
    to_frontend = {
        "user_active": True,
        "username": user.username,
        "uid": user.id,
        "userType": 'admin',
        "msg": "Welcome " + user.username + "!",
        "token": token,
        "building": '',
    }

    return Response(to_frontend)


@api_view(['POST'])
def createBuilding(request):
    # user
    # address
    # phone_number
    # num_of_apartments
    # num_of_tenants
    # service_charge_amount
    # total_fund

    print("data ", request.data)
    user = request.data['user']
    building = request.data['building']

    try:
        User(username=user['username'], password=make_password(user['password']), email=user['email']).save()
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
    # serializer = OwnerSerializer(owners, many=True)
    data = []

    for owner in owners:
        print(owner)
        apartment = Apartment.objects.filter(owner=owner)
        print('apartment', apartment.first())
        if apartment:
            floor_no = apartment.first().floor_number
            unit_no = apartment.first().apartment_number
        else:
            floor_no = None
            unit_no = None
        data.append({
            'owner_name': owner.user.first_name + ' ' + owner.user.last_name,
            'phone_number': owner.phone_number,
            'floor_no': floor_no,
            'unit_no': unit_no,
            'image': owner.get_image(),
        })

    to_frontend = {
        "data": data,
        "msg": "datafetched",
        "success": True,
    }

    return Response(to_frontend)


@api_view(['GET'])
def getOwner(request, pk):
    try:
        owner = Owner.objects.get(id=pk)
    except Owner.DoesNotExist:
        return Response(None)

    print(owner)
    serializer = OwnerSerializer(owner, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createOwner(request):
    print("data ", request.data)
    username = request.data['username']
    lastname = request.data['lastname']
    firstname = request.data['firstname']
    apartment_pk = request.data['apartment_pk']
    password = make_password(request.data['password'])
    email = request.data['email']
    phone_number = request.data['phone_number']
    bkash_acc_number = request.data['bkash_acc_number']
    image = request.data['image']

    user = None
    owner = None
    # get user

    to_frontend = {
        "error": "",
        "msg": "",
        "success": True,
    }

    try:
        # user already exists
        user = User.objects.get(username=username)

        to_frontend = {
            "error": "username",
            "msg": "username already exists",
            "success": False,
        }
        return Response(to_frontend)

    except User.DoesNotExist:

        # create owner
        # user
        try:
            User(username=username, password=password, email=email, last_name=lastname, first_name=firstname).save()
        except:
            print('Error: User object could not be created 1')
            to_frontend = {
                "error": "",
                "msg": "uknown error 1",
                "success": False,
            }
            return Response(to_frontend)
        user = User.objects.get(username=username)
        # user created by now

        # owner
        try:
            Owner(user=user, phone_number=phone_number, bkash_acc_number=bkash_acc_number).save()
        except:
            # delete created user
            User(username=username).delete()
            print('Error: Owner object could not be created 3')
            to_frontend = {
                "error": "",
                "msg": "uknown error 2",
                "success": False,
            }
            return Response(to_frontend)

        owner = Owner.objects.get(user=user)
        # user and owner created by now

    print(user, owner)
    # get apartment
    apartment = None
    try:
        apartment = Apartment.objects.get(id=apartment_pk)
    except:
        # delete created user and owner, should cascade and delete owner as well
        User(username=username).delete()

        print('Error: apartment not found 4')

        to_frontend = {
            "error": "",
            "msg": "uknown error 3",
            "success": False,
        }
        return Response(to_frontend)

    if apartment and user and owner:
        apartment.owner = owner
        apartment.save()
    else:
        # delete created user and owner, should cascade and delete owner as well
        User(username=username).delete()
        to_frontend = {
            "error": "",
            "msg": "uknown error 4",
            "success": False,
        }
        return Response(to_frontend)
    print(apartment)

    try:
        owner.image = image
        owner.save()
    except:
        to_frontend = {
            "error": "",
            "msg": "image not saved",
            "success": False,
        }
        return Response(to_frontend)
    return Response(to_frontend)


@api_view(['GET'])
def getAllApartmentsOfOwner(request, username):
    print(username)
    apartments = Apartment.objects.filter(owner__user__username=username)
    apartments = ApartmentSerializer(apartments, many=True).data

    return Response(apartments)


@api_view(['POST'])
def deleteOwner(request):
    pk = request.data['pk']

    try:
        owner = Owner.objects.get(id=pk)
    except Owner.DoesNotExist:
        #  no owner to remove
        to_frontend = {
            "msg": "no owner to remove",
            "success": False,
        }
        return Response(to_frontend)

    try:
        User(id=owner.user.id).delete()
    except:
        to_frontend = {
            "msg": "smth is wrong here",
            "success": False,
        }
        return Response(to_frontend)

    to_frontend = {
        "msg": "owner removed",
        "success": True,
    }
    return Response(to_frontend)


# --------------------------------------------------- Owner end ------------------------------------------------>>>
# --------------------------------------------------- Tenant start --------------------------------------------->>>

@api_view(['GET'])
def getAllTenants(request, username):
    try:
        tenants = Tenant.objects.all().filter(apartment__building__user__username=username)
    except:

        to_frontend = {
            "data": [],
            "msg": "datafetched",
            "success": True,
        }

        return Response(to_frontend)
    data = []

    for tenant in tenants:
        print(tenant)
        apartment = Apartment.objects.filter(tenant=tenant)
        print('apartment', apartment.first())
        if apartment:
            floor_no = apartment.first().floor_number
            unit_no = apartment.first().apartment_number
        else:
            floor_no = None
            unit_no = None
        data.append({
            'tenant_name': tenant.user.first_name + ' ' + tenant.user.last_name,
            'phone_number': tenant.phone_number,
            'floor_no': floor_no,
            'unit_no': unit_no,
            'image': tenant.get_image(),
        })

    to_frontend = {
        "data": data,
        "msg": "datafetched",
        "success": True,
    }

    return Response(to_frontend)


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
    username = request.data['username']
    lastname = request.data['lastname']
    firstname = request.data['firstname']
    apartment_pk = request.data['apartment_pk']
    password = make_password(request.data['password'])
    email = request.data['email']
    phone_number = request.data['phone_number']
    bkash_acc_number = request.data['bkash_acc_number']
    image = request.data['image']

    user = None
    tenant = None
    # get user

    to_frontend = {
        "error": "",
        "msg": "",
        "success": True,
    }

    try:
        # user already exists
        user = User.objects.get(username=username)

        to_frontend = {
            "error": "username",
            "msg": "username already exists",
            "success": False,
        }
        return Response(to_frontend)

    except User.DoesNotExist:

        # create tenant
        # user
        try:
            User(username=username, password=password, email=email, last_name=lastname, first_name=firstname).save()
        except:
            print('Error: User object could not be created 1')
            to_frontend = {
                "error": "",
                "msg": "uknown error 1",
                "success": False,
            }
            return Response(to_frontend)
        user = User.objects.get(username=username)
        # user created by now

        # tenant
        try:
            Tenant(user=user, phone_number=phone_number, bkash_acc_number=bkash_acc_number).save()
        except:
            # delete created user
            User(username=username).delete()
            print('Error: Tenant object could not be created 3')
            to_frontend = {
                "error": "",
                "msg": "uknown error 2",
                "success": False,
            }
            return Response(to_frontend)

        tenant = Tenant.objects.get(user=user)
        # user and tenant created by now

    print(user, tenant)
    # get apartment
    apartment = None
    try:
        apartment = Apartment.objects.get(id=apartment_pk)
    except Apartment.DoesNotExist:
        # delete created user and tenant, should cascade and delete tenant as well
        User(username=username).delete()

        print('Error: apartment not found 4')

        to_frontend = {
            "error": "",
            "msg": "uknown error 3",
            "success": False,
        }
        return Response(to_frontend)

    if apartment and user and tenant:
        apartment.tenant = tenant
        apartment.save()
    else:
        # delete created user and tenant, should cascade and delete tenant as well
        User(username=username).delete()
        to_frontend = {
            "error": "",
            "msg": "uknown error 4",
            "success": False,
        }
        return Response(to_frontend)
    print(apartment)

    try:
        tenant.image = image
        tenant.save()
    except:
        to_frontend = {
            "error": "",
            "msg": "image not saved",
            "success": False,
        }
        return Response(to_frontend)

    return Response(to_frontend)


@api_view(['POST'])
def deleteTenant(request):
    pk = request.data['pk']

    try:
        tenant = Tenant.objects.get(id=pk)
    except Tenant.DoesNotExist:
        #  no tenant to remove
        to_frontend = {
            "msg": "no tenant to remove",
            "success": False,
        }
        return Response(to_frontend)

    try:
        User(id=tenant.user.id).delete()
    except:
        to_frontend = {
            "msg": "smth is wrong here",
            "success": False,
        }
        return Response(to_frontend)

    to_frontend = {
        "msg": "tenant removed",
        "success": True,
    }
    return Response(to_frontend)

# --------------------------------------------------- Tenant end ----------------------------------------------->>>
