from venv import create
from django.urls import path
from .views import *

urlpatterns = [
    path('getAllElections/<str:username>', getAllElections, name='getAllElections'),
    path('getElection/<int:pk>', getElection, name='getElection'),
    path('getNominees/<int:key>', getNominees, name='getNominees'),
    path('createElection/<str:username>', createElection, name='createElection'),
    path('createNominee', createNominee, name='createNominee'),
    path('approveNominee', approveNominee, name='approveNominee'),
    path('castVote', castVote, name='castVote'),
    path('deleteElection/<int:pk>', deleteElection, name='deleteElection',),
    path('getElectionVote/<int:pk>', getElectionVote, name='getElectionVote'),
    path('isNominee/<int:pk>', isNominee, name='isNominee'),
    path('earlyStop/<int:pk>', earlyStop, name='earlyStop'),
    path('getCommitteeMembers/<str:username>', getCommitteeMembers, name= 'getCommitteeMembers'),
    path('createCommitteePosition/<str:username>', createCommitteePosition, name='createCommitteePosition'),
    path('getPositions/<str:username>', getPositions, name = 'getPositions'),
    path('updateAutoApprove/<int:pk>', updateAutoApprove, name='updateAutoApprove'),
    path('getAutoApprove/<int:pk>', getAutoApprove, name='getAutoApprove'),
]