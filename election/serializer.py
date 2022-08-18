from rest_framework import serializers
from .models import *


class CommitteeElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitteeElection
        fields = '__all__'
        
class NomineeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nominee
        fields = '__all__'
        
class CommitteeElectionVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitteeElectionVote
        fields = '__all__'
        
class CommitteeMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitteeMember
        fields = '__all__'