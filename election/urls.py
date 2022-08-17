from venv import create
from django.urls import path
from .views import *

urlpatterns = [
    path('getAllElections', getAllElections, name='getAllElections'),
    path('getElection/<int:pk>', getElection, name='getElection'),
    path('getNominees/<int:key>', getNominees, name='getNominees'),
    path('createElection', createElection, name='createElection'),
    path('createNominee', createNominee, name='createNominee'),
    path('approveNominee', approveNominee, name='approveNominee'),
    path('castVote', castVote, name='castVote'),
    path('deleteElection/<int:pk>', deleteElection, name='deleteElection',),
    path('getElectionVote/<int:pk>', getElectionVote, name='getElectionVote'),
    path('isNominee/<int:pk>', isNominee, name='isNominee'),
]