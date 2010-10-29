from django.db import models
from django.contrib.auth.models import User

from competition.models import Phase, Competition



#created by a contest organizer, at which point an email with a signup
#link is sent out to the invitee. when the create an account using the
#invited email, a Judge is created and added to the various phases
class JudgeInvitation(models.Model):

    #invitation to judge a specific phase
    this_phase_only = models.ForeignKey(Phase, related_name="judge_invitations")

    #invitations for the whole competition set you
    #as a judge for all phases
    competition = models.ForeignKey(Competition, related_name="judge_invitations")

    #who is invited. multiple invitations can exist
    #for the same email if they've been added to multiple
    #contests or phases.
    email = models.CharField(max_length=140)



#A "judge" role is a connection between a user and a single competition.
#If the same user was invited to multiple contests, then separate Judge
#objects would be used.
#
#However, only one judge object is used for multiple phases within a
#single competition.
class Judge(models.Model):

    #JudgeInvitations are accepted by creating an account, which makes a user
    user = models.ForeignKey(User)

    #set to True if the JudgeInvitation has this_phase_only=None
    #In this case, adding phases to a competition after the fact will give
    #permissions for them to this judge.
    is_judging_all_phases = models.BooleanField(default=False)

    #which phases I've got permissions to judge. These should all be within
    #a single competition
    phases = models.ManyToManyField(Phase, related_name="judges")
    


