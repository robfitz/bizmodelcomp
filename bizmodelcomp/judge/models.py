from django.db import models
from django.contrib.auth.models import User

from emailhelper.util import send_email
from utils.util import rand_key



#created by a contest organizer, at which point an email with a signup
#link is sent out to the invitee. when the create an account using the
#invited email, a Judge is created and added to the various phases
#
#if the same email is invited to multiple contests, then several JudgeInvitations
#can all point at the same User object.
class JudgeInvitation(models.Model):

    #invitation to judge a specific phase
    this_phase_only = models.ForeignKey("competition.Phase", related_name="judge_invitations", blank=True, null=True)

    #invitations for the whole competition set you
    #as a judge for all phases
    competition = models.ForeignKey("competition.Competition", related_name="judge_invitations")

    #who is invited. multiple invitations can exist
    #for the same email if they've been added to multiple
    #contests or phases.
    email = models.CharField(max_length=140)

    #only sends one email per person. This is set to a correct default
    #and changed automatically once the email gets set. Do NOT change directly.
    has_received_invite_email = models.BooleanField(default=False)

    #this is a list of all the phases that have alerted us that they're open
    #and we're ready to judge them. this is handy when judges are added to
    #a phase after judging has already opened, and for being double sure
    #that we don't annoy people by sending them multiple copies of the same note
    received_phase_judging_open_emails_from = models.ManyToManyField("competition.Phase", related_name="sent_judging_open_emails_to")

    #JudgeInvitations are accepted by creating an account, which makes a user.
    #user=None means that the invite hasn't yet been accepted.
    user = models.ForeignKey(User, null=True, blank=True)


    #sort out an appropriate way to identify this judge to other judges
    def display_name(self):
        if self.user:
            if self.user.name:
                return self.user.name
            else:
                return self.user.email.split('@')[0]

        else:
            return self.email.split('@')[0]


    #tell them they're a winner
    def send_invitation_email(self, judging_link):
        if not self.has_received_invite_email:
            self.has_received_invite_email = True
            self.save()

            subject = "Judging the %s" % self.competition.name
            message_markdown = """Hello,

You've been invited to help judge the %s. Judging will run from shortly after the application deadline at %s until as soon as all the applications have been assessed.

You can start judging at:

%s?e=%s

Thanks very much for the help!

Sincerely,
%s team""" % (self.competition.name,
              self.competition.current_phase.deadline,
              judging_link,
              self.email,
              self.competition.name)
        
            to_email = self.email

            send_email(subject, message_markdown, to_email)
        
        else:
            print "already sent judge invitation"
            pass


    def send_judging_open_email(self, phase):

        if phase in self.received_phase_judging_open_emails_from.all():

            #already sent an alert, so do nothing
            return False

        else:
            try:
                #key already exists?
                verification_key = VerificationKey.objects.filter(email=self.email)[0]
                verification_key.is_verified=True
            except:
                #doesn't exist, make a new one pointing to the email that's pre-approved
                verification_key = VerificationKey(key=rand_key(),
                                                   user=None,
                                                   email=self.email,
                                                   is_verified=True)
            #in either case, save changes
            verification_key.save()
            
            judging_path = "/judge/?ev=%s" % key
            
            to_email = self.email
            subject = "Judging now open for %s" % self.competition.name
            message_markdown = """Hello,

Judging for %s is now open and will run until %s or as soon as all the applications have been assessed.

The link below will ask you to create an account and then take you to start judging submitted pitches. To ensure that we know who you are, please register with the same email address that this note is being sent to (%s).

%s

Your help as a judge is hugely appreciated. Please don't hesistate to reply if you have any questions, problems, or concerns.

Sincerely,

%s team""" % (self.competition.name,
              self.competition.current_phase().judging_close,
              self.email,
              judging_link,
              self.competition.name)
        
            
            send_email(subject, message_markdown, to_email)


    def __unicode__(self):

        return self.email



#a set of JudgedAnswers related to a submitted pitch
class JudgedPitch(models.Model):

    pitch = models.ForeignKey("competition.Pitch", related_name="judgements")

    judge = models.ForeignKey(JudgeInvitation, related_name="judgements")

    feedback = models.CharField(max_length=2000, blank=True, null=True)

    overall_score = models.IntegerField(default=0)
    max_overall_score = models.IntegerField(default=5)

    def score(self):

        points = 0
        judged_answers = JudgedAnswer.objects.filter(judged_pitch=self)

        for ja in judged_answers:
            if ja.score:
                points += ja.score

        points += self.overall_score
        return points


#a judge's reaction to a single submitted answer
class JudgedAnswer(models.Model):

    judged_pitch = models.ForeignKey(JudgedPitch)

    #answer can be null if applicant didn't fill anything in or when it's a
    #judge-feedback-only question
    answer = models.ForeignKey("competition.PitchAnswer", blank=True, null=True)

    score = models.IntegerField(blank=True, null=True)

    feedback = models.CharField(max_length=1000, blank=True, null=True)



