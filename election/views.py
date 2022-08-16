from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from apartment.serializer import *
from user.serializer import *
from .models import *
from apartment.models import *
from user.models import *

from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET'])
def getAllElections(request):
    elections = CommitteeElection.objects.all()
    serializer = CommitteeElectionSerializer(elections, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getElection(request, pk):
    try:
        election = CommitteeElection.objects.get(id=pk)
    except CommitteeElection.DoesNotExist:
        return Response(None)

    serializer = CommitteeElectionSerializer(election, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getNominees(request, key):
    nominees = Nominee.objects.filter(committee_election=key)
    serializer = NomineeSerializer(nominees, many=True)
    
    data = [ dict(each) for each in serializer.data ]
    
    for each in data:
        each['owner_name'] = Owner.objects.get(pk=each.get('owner')).user.username
    
    print(data)
    
    return Response(data)


