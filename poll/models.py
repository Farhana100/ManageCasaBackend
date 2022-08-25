from optparse import Option
from django.db import models
from user.models import *
from apartment.models import *

# Create your models here.

class Poll(models.Model):
    id = models.AutoField(primary_key=True)
    building = models.ForeignKey(Building, null=False, on_delete=models.CASCADE)
    phase = models.CharField(max_length=30, null=True, blank=True)
    selected_option = models.TextField(blank=True)
    topic = models.TextField()
    description = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    vote_count = models.IntegerField(default=0)
    no_of_options = models.IntegerField(default=0)
    
    
    def __int__(self):
        return self.id

    class Meta:
        db_table = 'poll'
        
class Option(models.Model):
    poll = models.ForeignKey(Poll, null=False, on_delete=models.CASCADE)
    option_name = models.TextField()
    vote_count = models.IntegerField(default=0)

    
    def __int__(self):
        return self.option_name

    class Meta:
        db_table = 'option'
        
class PollVote(models.Model):
    poll = models.ForeignKey(Poll, null=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL)
    option_name = models.ForeignKey(Option, null=True, on_delete=models.SET_NULL)
    
    
    def __int__(self):
        return self.option

    class Meta:
        db_table = 'poll_vote'
        

