from django.db import models
from django.contrib.auth.models import User

from competition.models import Phase, Competition
from emailhelper.util import send_email



#created by a contest organizer, at which point an email with a signup
#link is sent out to the invitee. when the create an account using the
#invited email, a Judge is created and added to the various phases
class JudgeInvitation(models.Model):

    #invitation to judge a specific phase
    this_phase_only = models.ForeignKey(Phase, related_name="judge_invitations", blank=True, null=True)

    #invitations for the whole competition set you
    #as a judge for all phases
    competition = models.ForeignKey(Competition, related_name="judge_invitations")

    #who is invited. multiple invitations can exist
    #for the same email if they've been added to multiple
    #contests or phases.
    email = models.CharField(max_length=140)

    has_sent_invite_email = models.BooleanField(default=False)
    

    #tell them they're a winner
    def send_invitation_email(self, smtp=None):
        if not self.has_sent_invite_email:
            self.has_sent_invite_email = True
            self.save()

            subject = "Judging the %s" % self.competition.name
            message_markdown = """Hello,

You've been invited to help judge the %s. The judging period runs from %s until %s or as soon as all the applications have been assessed.

We'll send a second note as the judging begins with a link to take you to the founders' pitches.

Thanks very much for the help,

%s team""" % (self.competition.name,
              self.competition.current_phase().applications_close_judging_open,
              self.competition.current_phase().judging_close,
              self.competition.name)
        
            to_email = self.email

            send_email(subject, message_markdown, to_email, smtp=smtp)
        
        else:
            print "already sent judge invitation"
            pass



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
    


