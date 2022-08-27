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
@api_view(['POST'])
def createPoll(request, username):
    start = request.data['startData']
    end = request.data['endData']
    options = request.data['options']
    print(options)

    building = Building.objects.get(user__username=username)

    to_frontend = {
        "success": False,
        "msg": "",
    }

    obj = Poll()
    obj.building = building
    obj.phase = "Pending"
    obj.topic = request.data['topic']
    obj.description = request.data['description']
    obj.start_time = start
    obj.end_time = end
    obj.no_of_options = len(options)
    obj.save()
    print(obj.pk)
    
    #add option
    for each in options:
        opt_obj = Option()
        opt_obj.poll = obj
        opt_obj.option_name = each
        opt_obj.save()     

    to_frontend['success'] = True
    to_frontend['msg'] = "poll created successfully"
    return Response(to_frontend)
    
    
@api_view(['GET'])
def getAllPolls(request, username):
    current_time = timezone.now()
    building_id = Building.objects.get(user__username = username)
    polls = Poll.objects.filter(building=building_id)
    
    for each in polls:
        # poll ended
        if each.end_time < current_time and each.phase.lower() == "voting":
            Poll.objects.filter(pk = each.id).update(phase = "Ended")
            options = Option.objects.filter(poll = each.id)
            vote_max_count = 0;
            option_name = ""
            for opt in options:
                if opt.vote_count > vote_max_count:
                    vote_max_count = opt.vote_count
                    option_name = opt.option_name
                    
            Poll.objects.filter(pk = each.id).update(selected_option = option_name)
        
        
        elif(each.start_time < current_time and each.phase.lower() == "pending"):
            Poll.objects.filter(pk = each.id).update(phase = "Voting")
            
            
    serializer = PollSerializer(polls, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPoll(request, pk):
    poll = Poll.objects.get(id = pk)
    
    serializer = PollSerializer(poll, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getOptions(request, pk):
    options = Option.objects.filter(poll = pk)
    serializer = OptionSerializer(options, many=True)

    data = [dict(each) for each in serializer.data]

    return Response(data)

@api_view(['POST'])
def getPollVote(request, pk):
    name = request.data['votername']
    
    ownerID = Owner.objects.get(user__username = name)
    to_frontend = {
        "success": False,
        "msg": "",
        "vote_existed": False,
        "option": "",
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
    Poll.objects.filter(id = pk).update(phase = "Ended", end_time = timezone.now())
    to_frontend = {
        "success": True,
    }
    
    return Response(to_frontend)


@api_view(['POST'])
def castVotePoll(request, pk):
    option_name = request.data['option']
    voter = request.data['voter']
    print(option_name)
    print(voter)

    optionID = Option.objects.get(poll = pk, option_name = option_name['current'])
    voterID = Owner.objects.get(user__username=voter)
    poll = Poll.objects.get(id=pk)
    
    to_frontend = {
        "success": False,
        "msg": "",
    }
    
    if PollVote.objects.filter(poll = pk, owner = voterID).exists():
        alreadyselectedoption = PollVote.objects.get(poll = pk, owner = voterID).option_name
        PollVote.objects.filter(poll = pk, owner = voterID).update(option_name = optionID)
        
        print(alreadyselectedoption.option_name)
        print(option_name['current'])
        if alreadyselectedoption.option_name != option_name['current']:
            print("dhukechi")
            v_count = Option.objects.get(poll = pk, option_name = alreadyselectedoption.option_name).vote_count
            Option.objects.filter(poll = pk, option_name = alreadyselectedoption.option_name).update(vote_count = v_count - 1)
            v_count = Option.objects.get(poll = pk, option_name = option_name['current']).vote_count
            Option.objects.filter(poll = pk, option_name = option_name['current']).update(vote_count = v_count + 1)
            
        to_frontend['success'] = True
        to_frontend['msg'] = "vote casted successfully"
        print("vote cast")
        return Response(to_frontend)
        
    #increase vote count
    option_vote_count = Option.objects.get(option_name = option_name['current'],
                               poll=poll).vote_count
    poll_vote_count = Poll.objects.get(id=poll).vote_count
    
   

    obj = PollVote()
    obj.option_name = optionID
    obj.owner = voterID
    obj.poll = poll
    obj.save()
    obj_option = Option.objects.filter(option_name = option_name['current'],
                            poll=poll)
    obj_option.update(vote_count = option_vote_count+1) 
    obj_election = Poll.objects.filter(id=poll)
    obj_election.update(vote_count = poll_vote_count+1)
                               

    to_frontend['success'] = True
    to_frontend['msg'] = "vote casted successfully"
    print("vote cast")
    return Response(to_frontend)



