from django.urls import path
from .views import *

urlpatterns = [
    path('getAllElections', getAllElections, name='getAllElections'),
    path('getElection/<int:pk>', getElection, name='getElection'),
    
]