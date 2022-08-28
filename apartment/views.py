from tempfile import NamedTemporaryFile
from urllib.request import urlopen

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
    apartments = Apartment.objects.all().filter(building__user__username=username).order_by('floor_number',
                                                                                            'apartment_number')

    all_apartments = {}

    for apartment in apartments:
        image = ApartmentImage.objects.filter(apartment=apartment)
        if image:
            image = image[0].get_image()
        else:
            image = None

        if str(apartment.floor_number) in all_apartments:
            all_apartments[str(apartment.floor_number)].append({
                'id': apartment.id,
                'floor_number': apartment.floor_number,
                'apartment_number': apartment.apartment_number,
                'owner': str(apartment.owner),
                'tenant': str(apartment.tenant),
                'image': image
            })
        else:
            all_apartments[str(apartment.floor_number)] = [{
                'id': apartment.id,
                'floor_number': apartment.floor_number,
                'apartment_number': apartment.apartment_number,
                'owner': str(apartment.owner),
                'tenant': str(apartment.tenant),
                'image': image
            }]

    # print(all_apartments)
    return Response(all_apartments)


@api_view(['GET'])
def getAllApartmentsWithoutOwners(request, username):
    apartments = Apartment.objects.all().filter(building__user__username=username).order_by('floor_number',
                                                                                            'apartment_number')

    all_apartments = {}

    for apartment in apartments:
        if apartment.owner:
            continue
        all_apartments[
            "Floor no.: " + str(apartment.floor_number) + ', Apartment no.: ' + apartment.apartment_number] = {
            'id': apartment.id,
            'floor_number': apartment.floor_number,
            'apartment_number': apartment.apartment_number,
            'owner': str(apartment.owner),
            'tenant': str(apartment.tenant),
            'rent': apartment.rent,
        }

    print(all_apartments)
    return Response(all_apartments)


@api_view(['GET'])
def getAllApartmentsWithoutTenants(request, username):
    apartments = Apartment.objects.all().filter(building__user__username=username).order_by('floor_number',
                                                                                            'apartment_number')

    all_apartments = {}

    for apartment in apartments:
        if apartment.tenant:
            continue
        all_apartments[
            "Floor no.: " + str(apartment.floor_number) + ', Apartment no.: ' + apartment.apartment_number] = {
            'id': apartment.id,
            'floor_number': apartment.floor_number,
            'apartment_number': apartment.apartment_number,
            'owner': str(apartment.owner),
            'tenant': str(apartment.tenant),
            'rent': apartment.rent,
        }

    print(all_apartments)
    return Response(all_apartments)


@api_view(['GET'])
def getApartment(request, pk):
    to_frontend = {
        "none": True,
    }
    try:
        apartment = Apartment.objects.get(id=pk)
    except Apartment.DoesNotExist:
        return Response(to_frontend)

    # apartment images
    images = ApartmentImage.objects.all().filter(apartment=apartment)

    images = [img.get_image() for img in images]

    # print(images)

    to_frontend['apartment_pk'] = apartment.pk
    to_frontend['apartment_floor_number'] = apartment.floor_number
    to_frontend['apartment_number'] = apartment.apartment_number
    to_frontend['apartment_building_address'] = apartment.building.address
    to_frontend['apartment_images'] = images

    to_frontend['apartment_owner'] = apartment.owner
    if apartment.owner:
        to_frontend['apartment_owner'] = apartment.owner.pk
        to_frontend['owner_name'] = apartment.owner.user.first_name + ' ' + apartment.owner.user.last_name
        to_frontend['owner_bkash_acc_number'] = apartment.owner.bkash_acc_number
        to_frontend['owner_phone_number'] = apartment.owner.phone_number
        to_frontend['owner_image'] = apartment.owner.get_image()

    to_frontend['apartment_tenant'] = apartment.tenant
    if apartment.tenant:
        to_frontend['apartment_tenant'] = apartment.tenant.pk
        to_frontend['tenant_name'] = apartment.tenant.user.first_name + ' ' + apartment.tenant.user.last_name
        to_frontend['tenant_bkash_acc_number'] = apartment.tenant.bkash_acc_number
        to_frontend['tenant_phone_number'] = apartment.tenant.phone_number
        to_frontend['tenant_arrival_date'] = apartment.tenant.arrival_date
        to_frontend['tenant_departure_date'] = apartment.tenant.departure_date
        to_frontend['tenant_image'] = apartment.tenant.get_image()

    to_frontend['apartment_rent'] = apartment.rent
    to_frontend['service_charge_due_amount'] = apartment.service_charge_due_amount

    to_frontend['none'] = False

    return Response(to_frontend)


@api_view(['POST'])
def createApartment(request):
    building = request.data['building']
    floor_number = request.data['floor_number']
    apartment_number = request.data['apartment_number']
    rent = request.data['rent']
    service_charge_due_amount = request.data['service_charge_due_amount']
    images_count = request.data['images_count']

    print("test print --------------------------------")
    print(request.data)
    print(images_count)

    try:
        building = Building.objects.get(user__username=building)
    except Building.DoesNotExist:
        to_frontend = {
            'msg': 'Building does not exist',
            'error': True,
        }
        return Response(to_frontend)

    try:
        Apartment(building=building,
                  floor_number=floor_number,
                  apartment_number=apartment_number,
                  rent=rent,
                  service_charge_due_amount=service_charge_due_amount).save()
    except:
        to_frontend = {
            'msg': 'Apartment could not be created',
            'error': True,
        }
        return Response(to_frontend)

    print("no error upto this 1")
    try:
        apartment = Apartment.objects.filter(building=building,
                                             floor_number=floor_number,
                                             apartment_number=apartment_number)[0]
        print("debug ", apartment)
    except:
        to_frontend = {
            'msg': "what error??!!",
            'error': True,
        }
        return Response(to_frontend)

    for index in range(int(images_count)):
        filename = "img_" + str(index)
        print(filename, request.data[filename])
        try:
            ApartmentImage(apartment=apartment, image=request.data[filename]).save()
        except:
            to_frontend = {
                'msg': "no image error",
                'error': True,
            }
            return Response(to_frontend)

    to_frontend = {
        'msg': 'Apartment created successfully',
        'error': False,
    }
    return Response(to_frontend)


@api_view(['POST'])
def updateApartment(request):
    print(request.data)
    # to_frontend = {
    #     'msg': 'test',
    #     'error': True,
    # }
    # return Response(to_frontend)

    pk = request.data['pk']
    building = request.data['building']
    floor_number = request.data['floor_number']
    apartment_number = request.data['apartment_number']
    rent = request.data['rent']
    service_charge_due_amount = request.data['service_charge_due_amount']
    images_count = request.data['images_count']

    try:
        building = Building.objects.get(user__username=building)
    except Building.DoesNotExist:
        to_frontend = {
            'msg': 'Building does not exist',
            'error': True,
        }
        return Response(to_frontend)

    apartment = None
    try:
        apartment = Apartment.objects.get(id=pk)
    except:
        to_frontend = {
            'msg': 'Apartment does not exist',
            'error': True,
        }
        return Response(to_frontend)

    try:
        apartment.floor_number = floor_number
        apartment.apartment_number = apartment_number
        apartment.rent = rent
        apartment.service_charge_due_amount = service_charge_due_amount

        apartment.save()
    except:
        to_frontend = {
            'msg': "what error??!!",
            'error': True,
        }
        return Response(to_frontend)

    for index in range(int(images_count)):
        filename = "img_" + str(index)
        print(filename, request.data[filename])
        try:
            ApartmentImage(apartment=apartment, image=request.data[filename]).save()
        except:
            to_frontend = {
                'msg': "no image error",
                'error': True,
            }
            return Response(to_frontend)


    to_frontend = {
        'msg': 'Apartment updated successfully',
        'error': False,
    }
    return Response(to_frontend)


@api_view(['POST'])
def deleteApartment(request):
    print(request.data)
    apartment_pk = request.data['apartment_pk']

    try:
        apartment = Apartment.objects.get(id=apartment_pk)
        if apartment.owner:
            User(id=apartment.owner.user.id).delete()
        if apartment.tenant:
            User(id=apartment.tenant.user.id).delete()
        Apartment(id=apartment_pk).delete()
        to_frontend = {
            'msg': 'Apartment deleted',
            'success': True,
        }
        return Response(to_frontend)
    except:
        to_frontend = {
            'msg': 'Apartment could not be deleted',
            'success': False,
        }
        return Response(to_frontend)

# --------------------------------------------------- Building admin end --------------------------------------->>>
