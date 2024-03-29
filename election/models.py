# from turtle import position
from django.db import models
from user.models import *
from apartment.models import *

# Create your models here.

class CommitteeElection(models.Model):
    id = models.AutoField(primary_key=True)
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)
    phase = models.CharField(max_length=30, null=True, blank=True)
    elected_member = models.ForeignKey(Owner, blank=True, null=True, on_delete=models.SET_NULL)
    position = models.CharField(max_length=30, null=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    nomination_start_time = models.DateTimeField(null=True, blank=True)
    nomination_end_time = models.DateTimeField(null=True, blank=True)
    voting_start_time = models.DateTimeField(null=True, blank=True)
    voting_end_time = models.DateTimeField(null=True, blank=True)
    vote_count = models.IntegerField(default=0)
    no_of_candidates = models.IntegerField(default=0)
    autoapprove = models.BooleanField(default=False)
    
    
    def __int__(self):
        return self.id

    class Meta:
        db_table = 'committee_election'
        
        
class Nominee(models.Model):
    committee_election = models.ForeignKey(CommitteeElection, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL)
    approval_status = models.CharField(max_length=30, null=False)
    vote_count = models.IntegerField(default=0)

    
    def __int__(self):
        return self.owner

    class Meta:
        db_table = 'nominee'
        
class CommitteeElectionVote(models.Model):
    committee_election = models.ForeignKey(CommitteeElection, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL)
    nominee = models.ForeignKey(Nominee, null=True, on_delete=models.SET_NULL)
    
    
    def __int__(self):
        return self.owner

    class Meta:
        db_table = 'election_vote'
        
class CommitteePosition(models.Model):
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)
    position = models.CharField(max_length=30, null=False)
    
    def __int__(self):
        return self.position

    class Meta:
        db_table = 'committee_position'
        
        
class CommitteeMember(models.Model):
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)
    committee_election = models.ForeignKey(CommitteeElection, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL)
    position = models.CharField(max_length=30, null=False)
    status = models.CharField(max_length=30, null=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    
    def __int__(self):
        return self.committee_election

    class Meta:
        db_table = 'committee_member'