from turtle import position
from django.db import models
from user.models import *
from apartment.models import *

# Create your models here.

class CommitteeElection(models.Model):
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)
    phase = models.CharField(max_length=30, null=True)
    elected_member = models.ForeignKey(Owner, blank=True, null=True, on_delete=models.SET_NULL)
    position = models.CharField(max_length=30, null=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    nomination_start_time = models.DateTimeField(null=True)
    nomination_end_time = models.DateTimeField(null=True)
    voting_start_time = models.DateTimeField(null=True)
    voting_end_time = models.DateTimeField(null=True)
    vote_count = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.position

    class Meta:
        db_table = 'committee_election'
        
        
class Nominee(models.Model):
    committee_election_ID = models.ForeignKey(CommitteeElection, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, blank=True, null=True, on_delete=models.SET_NULL)
    approval_status = models.CharField(max_length=30, null=False)
    
    
    def __str__(self):
        return self.Committee_Election_ID

    class Meta:
        db_table = 'nominee'
        
class CommitteeElectionVote(models.Model):
    committee_election_ID = models.ForeignKey(CommitteeElection, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, blank=True, null=True, on_delete=models.SET_NULL)
    nominee = models.ForeignKey(Nominee, blank=True, null=True, on_delete=models.SET_NULL)
    
    
    def __str__(self):
        return self.Committee_Election_ID

    class Meta:
        db_table = 'election_vote'