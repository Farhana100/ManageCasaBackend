from nis import cat
from tkinter.messagebox import NO
from turtle import position
from urllib import request
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
        CommitteeElection(building=building,
                          phase="pending",
                          position=position,
                          nomination_start_time=nom_start,
                          nomination_end_time=nom_end,
                          voting_start_time=vote_start,
                          voting_end_time=vote_end).save()
    except:
        print('Error: User object could not be created 1')
        to_frontend['msg'] = "election not created!"
        return Response(to_frontend)

    to_frontend['success'] = True
    to_frontend['msg'] = "election created successfully"
    return Response(to_frontend)


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

@api_view(['POST'])
def deleteElection(request, pk):
    # electionID = request.data['electionID']
    print(pk)
    to_frontend = {
        "success": False,
        "msg": "",
    }
    
    try:
        CommitteeElection.objects.filter(id=pk).delete()
    except:
        print('election could not be cancelled')
        to_frontend['msg'] = "election not cancelled!"
        return Response(to_frontend)

    to_frontend['success'] = True
    to_frontend['msg'] = "election cancelled successfully"
    return Response(to_frontend)


@api_view(['POST'])
def createNominee(request):
    print("bleh: ", request.data)
    name = request.data['name']
    electionID = request.data['election_id']
    approval_status = request.data['approval_status']

    ownerID = Owner.objects.get(user__username=name)
    election = CommitteeElection(id=electionID)

    to_frontend = {
        "success": False,
        "msg": "",
    }

    #create election
    try:
        Nominee(owner=ownerID,
                committee_election=election,
                approval_status=approval_status).save()
    except:
        print('Error: Nominee object could not be created 1')
        to_frontend['msg'] = "nominee not created!"
        return Response(to_frontend)

    to_frontend['success'] = True
    to_frontend['msg'] = "nominee created successfully"
    print("nominee created")
    return Response(to_frontend)


@api_view(['GET'])
def getNominees(request, key):
    nominees = Nominee.objects.filter(committee_election=key)
    serializer = NomineeSerializer(nominees, many=True)

    data = [dict(each) for each in serializer.data]

    for each in data:
        each['owner_name'] = Owner.objects.get(
            pk=each.get('owner')).user.username

    print(data)

    return Response(data)


@api_view(['POST'])
def approveNominee(request):
    print("bleh: ", request.data)
    name = request.data['name']
    electionID = request.data['election_id']
    approval_status = request.data['approval_status']

    ownerID = Owner.objects.get(user__username=name)
    election = CommitteeElection(id=electionID)

    to_frontend = {
        "success": False,
        "msg": "",
    }

    try:
        Nominee.objects.filter(owner=ownerID,
                               committee_election=election).update(
                                   approval_status=approval_status)
    except:
        print('Error: Nominee object could not be created 1')
        to_frontend['msg'] = "nominee not approved!"
        return Response(to_frontend)

    to_frontend['success'] = True
    to_frontend['msg'] = "nominee approved successfully"
    print("nominee approved")
    return Response(to_frontend)


@api_view(['POST'])
def castVote(request):
    print("bleh: ", request.data)
    name = request.data['name']
    electionID = request.data['electionID']
    voter = request.data['voter']

    nomineeOwner = Owner.objects.get(user__username=name)
    nomineeID = Nominee.objects.get(owner=nomineeOwner)
    voterID = Owner.objects.get(user__username=voter)
    election = CommitteeElection.objects.get(id=electionID)
    
    #increase vote count
    nom_vote_count = Nominee.objects.get(owner=nomineeOwner,
                               committee_election=election).vote_count
    election_vote_count = CommitteeElection.objects.get(id=election).vote_count
    
    to_frontend = {
        "success": False,
        "msg": "",
    }

    print(voterID)
    print(nomineeID)
    print(election)

    # add committe election vote
    try:
        obj = CommitteeElectionVote()
        obj.nominee = nomineeID
        obj.owner = voterID
        obj.committee_election = election
        obj.save()
        
        obj_nom = Nominee.objects.filter(owner=nomineeOwner,
                                committee_election=election)
        obj_nom.update(vote_count = nom_vote_count+1) 
        
        obj_election = CommitteeElection.objects.filter(id=election)
        obj_election.update(vote_count = election_vote_count+1)
                               
    except:
        print('Error: Vote object could not be created 1')
        to_frontend['msg'] = "vote not casted!"
        return Response(to_frontend)

    to_frontend['success'] = True
    to_frontend['msg'] = "vote casted successfully"
    print("vote cast")
    return Response(to_frontend)


@api_view(['GET'])
def getVoteInfo():
    return Response(None)
