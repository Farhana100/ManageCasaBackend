from turtle import position
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

from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def createElection(request, username):
    position = request.data['positionData']
    nom_start = request.data['nomstartData']
    nom_end = request.data['nomendData']
    vote_start = request.data['votestartData']
    vote_end = request.data['voteendData']
    auto_approve = request.data['autoapprove']

    building = Building.objects.get(user__username=username)

    to_frontend = {
        "success": False,
        "msg": "",
    }
    
    if(auto_approve == "true"):
        auto_approve = True
    else:
        auto_approve = False

    #create election
    CommitteeElection(building=building,
                        phase="Pending",
                        position=position,
                        nomination_start_time=nom_start,
                        nomination_end_time=nom_end,
                        voting_start_time=vote_start,
                        voting_end_time=vote_end,
                        autoapprove=auto_approve).save()

    to_frontend['success'] = True
    to_frontend['msg'] = "election created successfully"
    return Response(to_frontend)


@api_view(['GET'])
def getAllElections(request, username):
    current_time = timezone.now()
    building_id = Building.objects.get(user__username = username)
    elections = CommitteeElection.objects.filter(building=building_id)
    print(elections)
    
    for each in elections:
        #voting end time < current time
        if each.voting_end_time <= current_time and each.phase.lower() == "voting":
            CommitteeElection.objects.filter(pk = each.id).update(phase = "Ended")
            nominees = Nominee.objects.filter(committee_election = each.id)
            vote_max_count = 0;
            nominee_id = ""
            for nom in nominees:
                if nom.vote_count > vote_max_count:
                    vote_max_count = nom.vote_count
                    nominee_id = nom.owner
            
            CommitteeElection.objects.filter(pk = each.id).update(elected_member = nominee_id)
                
            CommitteeMember.objects.filter(building=building_id, position=each.position).update(status = "inactive")
            obj = CommitteeMember()
            obj.building = building_id
            obj.committee_election = each
            obj.owner = nominee_id
            obj.position = each.position
            obj.status = "active"
            obj.start_date = timezone.now()
            obj.save()
            
            
        #voting start time < current time
        elif each.voting_start_time <= current_time and (each.phase.lower() == "pending" or each.phase.lower() == "nomination"):
            CommitteeElection.objects.filter(pk = each.id).update(phase = "Voting")
            
        #nomination end time < current time
        elif each.nomination_end_time <= current_time and each.phase.lower() == "nomination":
            CommitteeElection.objects.filter(pk = each.id).update(phase = "Pending")
            
        #nomination start time < current time
        elif each.nomination_start_time <= current_time and each.phase.lower() == "pending":
            CommitteeElection.objects.filter(pk = each.id).update(phase = "nomination")
    
    serializer = CommitteeElectionSerializer(elections, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getElection(request, pk):
    election = CommitteeElection.objects.get(id=pk)

    serializer = CommitteeElectionSerializer(election, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def updateAutoApprove(request, pk):
    print(request.data['autoapprove'])
    CommitteeElection.objects.filter(id=pk).update(autoapprove=request.data['autoapprove'])
    
    Nominee.objects.filter(committee_election=pk, approval_status = "Pending").update(approval_status = "Approved")
    
    to_frontend = {
        "success": True,
        "msg": " auto approval updated"
    }
    return Response(to_frontend)

@api_view(['GET'])
def getAutoApprove(request, pk):
    autoapprove = CommitteeElection.objects.get(id=pk).autoapprove
    to_frontend = {
        'success': True,
        'msg': "fetched",
        'autoapprove': autoapprove
    }
    
    return Response(to_frontend)
    
    
@api_view(['POST'])
def deleteElection(request, pk):
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
    name = request.data['name']
    electionID = request.data['election_id']
    approval_status = request.data['approval_status']

    ownerID = Owner.objects.get(user__username=name)
    election = CommitteeElection(id=electionID)
    
    autoapprove = CommitteeElection.objects.get(id=electionID).autoapprove
    if(autoapprove == True):
        approval_status = "Approved"
    print(approval_status)

    to_frontend = {
        "success": False,
        "msg": "",
    }

    #create nominee
    Nominee(owner=ownerID,
            committee_election=election,
            approval_status=approval_status).save()
    

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
        each['image'] = Owner.objects.get(pk = each.get('owner')).get_image()

    return Response(data)


@api_view(['POST'])
def approveNominee(request):
    name = request.data['name']
    electionID = request.data['election_id']
    approval_status = request.data['approval_status']

    ownerID = Owner.objects.get(user__username=name)
    election = CommitteeElection(id=electionID)
    
    candidate_no = CommitteeElection.objects.get(id=electionID).no_of_candidates

    to_frontend = {
        "success": False,
        "msg": "",
    }

    try:
        Nominee.objects.filter(owner=ownerID,
                               committee_election=election).update(
                                   approval_status=approval_status)
        CommitteeElection.objects.filter(id=electionID).update(no_of_candidates = candidate_no + 1)
    except:
        print('Error: Nominee object could not be created 1')
        to_frontend['msg'] = "nominee not approved!"
        return Response(to_frontend)

    to_frontend['success'] = True
    to_frontend['msg'] = "nominee approved successfully"
    print("nominee approved")
    return Response(to_frontend)

@api_view(['POST'])
def updatenomstart(request, pk):
    print("dhukechi")
    nomstart = request.data['nomstart']
    CommitteeElection.objects.get(id=pk).update(nomination_start_time=nomstart)
    to_frontend = {
        'success': True,
        'msg': "updated",
    }
    
    return Response(to_frontend)

@api_view(['POST'])
def castVote(request):
    name = request.data['name']
    electionID = request.data['electionID']
    voter = request.data['voter']

    nomineeOwner = Owner.objects.get(user__username=name)
    nomineeID = Nominee.objects.get(owner=nomineeOwner, committee_election = electionID)
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
                               

    to_frontend['success'] = True
    to_frontend['msg'] = "vote casted successfully"
    print("vote cast")
    return Response(to_frontend)


@api_view(['POST'])
def getElectionVote(request, pk):
    name = request.data['votername']
    
    ownerID = Owner.objects.get(user__username = name)
    to_frontend = {
        "success": False,
        "msg": "",
        "vote_existed": False,
        "nominee": "",
    }
    
    if CommitteeElectionVote.objects.filter(committee_election = pk, owner = ownerID).exists():
        nom_obj = CommitteeElectionVote.objects.get(committee_election = pk, owner = ownerID).nominee
        owner_name = nom_obj.owner
        nom_name = owner_name.user.username
        print(type(nom_name))
        print(name)
        to_frontend['success'] = True
        to_frontend['msg'] = "vote existed"
        to_frontend['vote_existed'] = True
        to_frontend['nominee'] = nom_name
        print("vote existed")
        return Response(to_frontend)
    
    to_frontend['msg'] = "vote not existed"
    to_frontend['success'] = True
    print("vote not existed")
    return Response(to_frontend)


@api_view(['POST'])
def isNominee(request, pk):
    name = request.data['nominee_name']
    
    ownerID = Owner.objects.get(user__username = name)
    to_frontend = {
        "success": False,
        "msg": "",
        "nominee_existed": False,
    }
    
    if Nominee.objects.filter(committee_election = pk, owner = ownerID).exists():
        to_frontend['success'] = True
        to_frontend['msg'] = "nominee existed"
        to_frontend['nominee_existed'] = True
        print("nominee existed")
        return Response(to_frontend)
    
    to_frontend['msg'] = "nominee not existed"
    to_frontend['success'] = True
    print("nominee not existed")
    return Response(to_frontend)


@api_view(['POST'])
def earlyStop(request, pk):
    CommitteeElection.objects.filter(pk = pk).update(phase = "Ended", voting_end_time = timezone.now())
    to_frontend = {
        "success": True,
    }
    
    return Response(to_frontend)


@api_view(['POST'])
def createCommitteePosition(request, username):
    position = request.data['position']
    building_id = Building.objects.get(user__username = username)
    positions = CommitteePosition.objects.filter(building = building_id)
    
    to_frontend = {
        "success": False,
        "msg": "",
    }
    
    for each in positions:
        if(each.position == position):
            to_frontend['msg'] = "Position Already Exists"
            return Response(to_frontend)
        
    obj = CommitteePosition()
    obj.building = building_id
    obj.position = position
    obj.save()
    
    to_frontend = {
        "success": True,
        "msg": position + "Position Created Successfully",
    }
    return Response(to_frontend)
    
@api_view(['GET'])
def getPositions(request, username):
    building_id = Building.objects.get(user__username = username)
    positions = CommitteePosition.objects.filter(building = building_id)
     
    pos_data = []
    for pos in positions:
        pos_data.append({
            "positions": pos.position
        })
        
        
    to_frontend = {
        "success": True,
        "msg": "position fetched",
        "positions": pos_data, 
    }
    
    return Response(to_frontend)

@api_view(['GET'])
def getCommitteeMembers(request, username):
    building_id = Building.objects.get(user__username=username)
    committeemembers = CommitteeMember.objects.filter(building=building_id, status="active")
    committeeposition = CommitteePosition.objects.filter(building=building_id)
    
    data = []
    
    for member in committeemembers:
        apartment = Apartment.objects.filter(owner=member.owner)
        print('apartment', apartment.first())
        if apartment:
            floor_no = apartment.first().floor_number
            unit_no = apartment.first().apartment_number
        else:
            floor_no = None
            unit_no = None
        data.append({
            'position': member.position,
            'owner_name': member.owner.user.username,
            'start_date': member.start_date,
            'floor_no': floor_no,
            'unit_no': unit_no,
            'image': member.owner.get_image(),
        })
        
    for position in committeeposition:
        existPosition = False
        for everydata in data:
            if(position.position == everydata['position']):
                existPosition = True
                break
        if(existPosition == False):
            data.append({
                'position': position.position,
                'owner_name': "",
            })
    print(data)
    to_frontend = {
        "data": data,
        "msg": "datafetched",
        "success": True,
    }

    return Response(to_frontend)
    