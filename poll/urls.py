from venv import create
from django.urls import path
from .views import *

urlpatterns = [
    path('getAllPolls/<str:username>', getAllPolls, name = 'getAllPolls'),
    path('getPoll/<int:pk>', getPoll, name = 'getPoll'),
    path('getOptions/<int:pk>', getOptions, name = 'getOptions'),
    path('getPollVote/<int:pk>', getPollVote, name = 'getPollVote'),
    path('deletePoll/<int:pk>', deletePoll, name = 'deletePoll'),
    path('earlyStopPoll/<int:pk>', earlyStopPoll, name = 'earlyStopPoll'),
    path('castVotePoll', castVotePoll, name = 'castVotePoll'),
]
