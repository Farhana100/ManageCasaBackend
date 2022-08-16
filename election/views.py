from turtle import position
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

@api_view(['POST'])
def createElection(request):
    print(request.data)
    position = request.data['positionData']
    nom_start = request.data['nomstartData']
    nom_end = request.data['nomendData']
    vote_start = request.data['votestartData']
    vote_end = request.data['voteendData']
    
    building = Building.objects.get(user__username="building1")
    
    
    to_frontend = {
        "success": False,
        "msg": "",
        
    }
    
    #create election
    try:
        CommitteeElection(building = building, phase = "pending", position=position, nomination_start_time = nom_start, nomination_end_time = nom_end, voting_start_time = vote_start, voting_end_time = vote_end).save()
    except:
        print('Error: User object could not be created 1')
        to_frontend['msg'] = "election not created!"
        return Response(to_frontend)
    
    to_frontend['success'] = True;
    to_frontend['msg'] = "election created successfully" ;
    return Response(to_frontend)

