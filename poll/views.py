from django.shortcuts import render
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
def getAllPolls(request, username):
    building_id = Building.objects.get(user__username = username)
    polls = Poll.objects.filter(building=building_id)
    
    serializer = PollSerializer(polls, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPoll(request, pk):
    poll = Poll.objects.get(id = pk)
    
    serializer = PollSerializer(poll, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def deletePoll(request, pk):
    to_frontend = {
        "success": False,
        "msg": "",
    }

    Poll.objects.filter(id=pk).delete()
    

    to_frontend['success'] = True
    to_frontend['msg'] = "poll cancelled successfully"
    return Response(to_frontend)


@api_view(['POST'])
def earlyStopPoll(request, pk):
    Poll.objects.filter(id = pk).update(phase = "ended", end_time = timezone.now())
    to_frontend = {
        "success": True,
    }
    
    return Response(to_frontend)


@api_view(['GET'])
def getOptions(request, pk):
    options = Option.objects.filter(poll = pk)
    serializer = OptionSerializer(options, many=True)

    data = [dict(each) for each in serializer.data]

    return Response(data)

@api_view(['POST'])
def castVotePoll(request):
    option_name = request.data['option_name']
    pollID = request.data['pollID']
    voter = request.data['voter']

    optionID = Option.objects.get(poll = pollID, option_name = option_name)
    voterID = Owner.objects.get(user__username=voter)
    poll = Poll.objects.get(id=pollID)
    
    #increase vote count
    option_vote_count = Option.objects.get(option_name = option_name,
                               poll=poll).vote_count
    poll_vote_count = Poll.objects.get(id=poll).vote_count
    
    to_frontend = {
        "success": False,
        "msg": "",
    }

    obj = PollVote()
    obj.option_name = optionID
    obj.owner = voterID
    obj.poll = poll
    obj.save()
    obj_nom = Option.objects.filter(option_name = option_name,
                            poll=poll)
    obj_nom.update(vote_count = option_vote_count+1) 
    obj_election = Poll.objects.filter(id=poll)
    obj_election.update(vote_count = poll_vote_count+1)
                               

    to_frontend['success'] = True
    to_frontend['msg'] = "vote casted successfully"
    print("vote cast")
    return Response(to_frontend)



@api_view(['POST'])
def getPollVote(request, pk):
    name = request.data['votername']
    
    ownerID = Owner.objects.get(user__username = name)
    to_frontend = {
        "success": False,
        "msg": "",
        "vote_existed": False,
        "nominee": "",
    }
    
    if PollVote.objects.filter(poll = pk, owner = ownerID).exists():
        option = PollVote.objects.get(poll = pk, owner = ownerID).option_name
        option_name = option.option_name
        owner = PollVote.objects.get(poll = pk, owner = ownerID).owner
        owner_name = owner.user.username
        print(type(option_name))
        print(owner_name)
        to_frontend['success'] = True
        to_frontend['msg'] = "vote existed"
        to_frontend['vote_existed'] = True
        to_frontend['option'] = option_name
        print("vote existed")
        return Response(to_frontend)
    
    to_frontend['msg'] = "vote not existed"
    to_frontend['success'] = True
    print("vote not existed")
    return Response(to_frontend)