from rest_framework import serializers
from .models import *

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'
        
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'
        
class PollVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollVote
        fields = '__all__'