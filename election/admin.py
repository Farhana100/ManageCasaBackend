from django.contrib import admin
from .models import *

class CommitteeElectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'building', 'phase', 'elected_member', 'position', 'creation_time', 'nomination_start_time', 'nomination_end_time', 'voting_start_time', 'voting_end_time', 'vote_count', 'no_of_candidates', 'autoapprove')

class NomineeAdmin(admin.ModelAdmin):
    list_display = ('committee_election', 'owner', 'approval_status', 'vote_count')
    
class CommitteeElectionVoteAdmin(admin.ModelAdmin):
    list_display = ('committee_election', 'owner', 'nominee')
    
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('building', 'committee_election', 'owner', 'position','status', 'start_date', 'end_date')
    
class CommitteePositionAdmin(admin.ModelAdmin):
    list_display = ('building', 'position')
    
admin.site.register(CommitteeElection, CommitteeElectionAdmin)
admin.site.register(Nominee, NomineeAdmin)
admin.site.register(CommitteeElectionVote, CommitteeElectionVoteAdmin)
admin.site.register(CommitteeMember, CommitteeMemberAdmin)
admin.site.register(CommitteePosition, CommitteePositionAdmin)