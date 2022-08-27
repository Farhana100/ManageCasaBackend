from django.contrib import admin
from .models import *

# Register your models here.
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'building', 'phase', 'selected_option', 'topic', 'description', 'creation_time', 'end_time', 'vote_count', 'no_of_options')

class OptionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'option_name', 'vote_count')
    
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'owner', 'option_name')
    
admin.site.register(Poll, PollAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(PollVote, PollVoteAdmin)