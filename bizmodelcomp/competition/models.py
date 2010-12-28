from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from itertools import chain

import string
import array
import sys
import time

from settings import MEDIA_URL
from utils.util import *
from judge.models import *

from django.forms import ModelForm


#guy with a business model who is developing it, applying
#for contests, or getting feedback from peers
class Founder(models.Model):

    user = models.OneToOneField(User, blank=True, null=True)

    name = models.CharField(max_length=500, blank=True, null=True) #don't use first/last/etc for multi-cultural reasons
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    #isoformat yyyy-mm-dd
    birth = models.CharField(max_length=10, blank=True, null=True) #representation of a datetime

    #If False, anyone can create or edit a pitch for this founder
    #by simply knowing and entering the matching email address.
    #This is generally undesired, so the default (and standard) value is
    #true.
    #It should be set to False when we have loaded applicant data
    #from an external source like a CSV file and they haven't yet registered
    #through us.
    #Once they submit the first pitch version, this flag should
    #be fkipped back to True to prevent unauthorized editing.
    require_authentication = models.BooleanField(default=True)


    #get or create randomized anonymous login key
    def anon_key(self):
        key = None

        try:
            key = AnonymousFounderKey.objects.get(founder=self)
        except:
            random_key = rand_key()
            key = AnonymousFounderKey(founder=self, key=random_key)
            key.save()
            
        return key


    #returns the set of ExtraFounderInfos attached to this Founder as
    #a dictionary of question:answer pairs 
    def extra(self):
        dictionary = {}
        for info in self.extra_info.all():
           dictionary[info.question.prompt] = info.answer
        return dictionary
        

    def __unicode__(self):

        return self.email



#one lead founder, plus some info about the team and any additional founders
class Team(models.Model):

    owner = models.ForeignKey(Founder, related_name="owner_set")

    other_members = models.ManyToManyField(Founder)

    name = models.CharField(max_length="140", default="", blank=True)


    def members(self):
        members = [self.owner]
        members.extend(self.other_members.all())

        return members



#a random key used in links to take an applicant
#to their application without needing to create an account
class AnonymousFounderKey(models.Model):

    #random characters used as an identifier
    key = models.CharField(max_length=20, primary_key=True) 
    founder = models.OneToOneField(Founder) #who i point to


    def __unicode__(self):

        return self.key



#a business model competition
class Competition(models.Model):

    name = models.CharField(max_length=500, blank=True, default="")
    website =  models.CharField(max_length=500, blank=True, default="")
    hosted_url = models.CharField(max_length=100, unique=True)

    owner = models.ForeignKey(User) #single owner who can delete it
    applicants = models.ManyToManyField(Founder, related_name="competitions", blank=True, null=True) #info about peeps entered in contest

    current_phase = models.OneToOneField("competition.Phase", blank=True, null=True, related_name="competition_unused")

    #branding
    logo = models.FileField(null=True, blank=True, upload_to="uploads/logos/")

    #more branding, only used for totally custom whitelabelling
    template_base = models.CharField(max_length=200, default="base.html")
    template_pitch = models.CharField(max_length=201, default="entercompetition/pitch_form.html")
    template_stylesheet = models.CharField(max_length=200, blank=True, default="")


    def logo_url(self):

        if self.logo:
            return "%s%s" % (MEDIA_URL, self.logo) 
        else:
            return None


    def phases(self):

	    return Phase.objects.filter(competition=self).filter(is_deleted=False)


    def first_phase(self):

        return self.phases()[0]
    

    def pitches(self):

        unsorted = self.current_phase.pitches.all()
        
##        sorted_pitches = []
##    
##        for u in unsorted:
##            inserted = False
##            
##            for s in sorted_pitches:
##                if u.average_score() >= s.average_score():
##                    sorted_pitches.insert(sorted_pitches.index(s), u)
##                    inserted = True
##                    break
##
##            if not inserted:
##                sorted_pitches.append(u)
##
##        return sorted_pitches

        return unsorted
    

    def is_judging_open(self):

        #judging is always open for live pitches, since there's nothing to submit.
        #it needs to be explicitly set for online phases.
        return self.current_phase and (self.current_phase.is_judging_enabled or self.current_phase.pitch_type == "live pitch")


    def __unicode__(self):

        return self.name



PHASE_STATUS_CHOICES = (('pending', 'pending'),
                        ('accepting pitches', 'accepting pitches'),
                        ('being judged', 'being judged'),
                        ('choosing winners', 'choosing winners'),
                        ('completed', 'completed'))

PHASE_PITCH_TYPES = [('online', 'online'),
                     ('live pitch', 'live pitch' )]

#a subset of a competition, which involves applicants submitting
#some form of pitch which is then judged
class Phase(models.Model):

    competition = models.ForeignKey(Competition, editable=False, related_name="all_phases")
    name = models.CharField(max_length=140, blank=True, default="")

    deadline = models.DateTimeField(default=datetime.now())

    pitch_type = models.CharField(max_length=20, choices=PHASE_PITCH_TYPES, default="online")

    #a manual throw switch that an organizer can flip to kick off the judging
    #period. This variable gives them a way to, for example, review applications
    #or organize themselves before auto-alerting all the judges
    #
    #for it to do anything, the current time should also be between applications_close
    #and judging_close.
    is_judging_enabled = models.BooleanField(default=False)

    #when an organizer deletes a phase, we just set this flag so we can recover
    #their data if needed
    is_deleted = models.BooleanField(default=False)

    #current_status = models.CharField(max_length=140,
    #                                  choices=PHASE_STATUS_CHOICES,
    #                                  default='pending')

    min_judgements_per_pitch = models.IntegerField(default=2)

    #note: related_name for M2M relation w/ alerted judges is: sent_judging_open_emails_to

    def setup_steps(self):

        try:
            steps = PhaseSetupSteps.objects.get(phase=self)
        except:
            steps = PhaseSetupSteps(phase=self)
            steps.save()

        print 'phase %s setup steps: %s' % (self.id, steps.id)
            
        return steps
        

    def deadline_date_js(self):

        return int(time.mktime(self.deadline.timetuple())*1000)
    

    def max_score(self):
        
        max_score = 0
        for question in PitchQuestion.objects.filter(phase=self):    
            max_score += question.max_points

        return max_score


    #returns a string button/link label that hints at what the organizer should do
    #next to keep the competition ticking forward
    def current_status_call_to_action(self):

        if self.competition.current_phase == self:

            if self.current_status == 'pending':
                return 'Begin accepting pitches'
            elif self.current_status == 'accepting pitches':
                return 'Begin judging'
            elif self.current_status == 'being judged':
                return 'Choose winners'
            elif self.current_status == 'choosing winners':
                return 'Conclude this phase'

        return ''


    #scoot this phase's current_status forward a notch. if it
    #has reached the final status and is currently the active
    #phase for the competition, it also bumps the competition
    #forward to the next phase
    def begin_next_state(self):

        if self.current_status == 'pending':
            self.current_status = 'accepting pitches'
            
        elif self.current_status == 'accepting pitches':
            self.current_status = 'being judged'
            
        elif self.current_status == 'being judged':
            self.current_status = 'choosing winners'
            
        elif self.current_status == 'choosing winners':
            self.current_status = 'completed'

            #get next phase
            phases = self.competition.phases()
            i = phases.index(self)
            if i + 1 < len(phases):
                next_phase = phases[i + 1]
                if self.competition.current_phase == self:
                    self.competition.current_phase = next_phase
                    self.competition.save()
                    
        self.save()
            

    #returns a list of the most active judges for this competition phase,
    #along with how many items they've judged and the average score given
    def judge_leaderboard(self, num_leaders=5):
        
        leaderboard = []
        
        for judge in self.judges():
            judgements = JudgedPitch.objects.filter(judge=judge).filter(pitch__phase=self)
            total_score = 0
            for j in judgements:
                total_score = total_score + j.score()

            if judge and judgements and len(judgements) > 0:
                leaderboard.append({'judge': judge, 'num_judged': len(judgements), 'average_score': float(total_score) / len(judgements) })

        if num_leaders == -1:
            return leaderboard
        else:
            return leaderboard[:num_leaders]


    def judge_rank(self, judge):

        rank = 0
        
        for leader in self.judge_leaderboard(-1):
            if leader['judge'] == judge:
                return '%s<sup>%s</sup>' % (rank, ordinal(rank)[1:])
            rank += 1

        return "N/A"
    
    
    def judgements(self, for_judge=None, num=10):
        
        pitches = Pitch.objects.filter(phase=self)
        judgements = []
        
        for pitch in pitches:
            
            if for_judge:
                judgements.extend(pitch.judgements.filter(judge=for_judge))
            else:
                judgements.extend(pitch.judgements.all())

        if num > 0:
            return judgements[-num:]
        else:
            return judgements


    #get list of all applications yet to be judged enough times
    def pitches_to_judge(self, for_judge=None):
        
        pitches = Pitch.objects.filter(phase=self)
        to_judge = []

        print '%s pitches for phase id=%s' % (len(pitches), self.id)
        
        organizer = self.competition.owner
        
        for pitch in pitches:
        
            if pitch.judgements.count() < self.min_judgements_per_pitch:
                #if a pitch has been judged enough, no one needs to deal with it
                
                if for_judge is not None:
                    #if we're looking for pitches a particular judge needs to look at,
                    #we also disregard the stuff he's already cast judgement on
                    
                    #if pitch.judgements.filter(judge=for_judge).count() == 0:
                    if JudgedPitch.objects.filter(judge=for_judge).filter(pitch=pitch).count() == 0:
                        to_judge.append(pitch)
                    
                else:
                    #if we don't care about a particular judge, everything without
                    #enough votes counts
                    to_judge.append(pitch)
                
        return to_judge


    def judges(self):

        comp_judges = JudgeInvitation.objects.filter(competition=self.competition)
        my_judges = []
        
        for comp_judge in comp_judges:

            if comp_judge.this_phase_only == self:

                    my_judges.append(comp_judge)

            elif not comp_judge.this_phase_only:

                my_judges.append(comp_judge)

        return my_judges

                
    #tell any judges for this phase who haven't been alerted yet that
    #judging is open and ready for their wonderful assistance
    def send_judging_open_emails(self):

        for judge in self.judges():

            judge.send_judging_open_email(self)

            
    #timestamp for whenever the next thing is going to close (organization,
    #applications, judging, etc)
    def next_deadline(self):

        if datetime.now() < self.applications_open:
            return self.applications_open

        elif datetime.now() < self.applications_close_judging_open:
            return self.applications_close_judging_open

        elif datetime.now() < self.judging_close():
            return self.judging_close

        else: return 0
    

    def time_left(self):

        return self.next_deadline() - datetime.now()


    def questions(self):

        return self.pitchquestion_set.all()


    def uploads(self):

        return self.pitchupload_set.all()


    def judging_criteria(self): 

        return self.pitchquestion_set.all()
    
    
    #TODO: make this better (currently everyone is in every phase)
    def applicants(self):

        return self.competition.applicants.all()

    def __unicode__(self):

        return "phase (id=%s) for (competition=%s)" % (self.pk, self.competition)
    

class PhaseSetupSteps(models.Model):

    phase = models.OneToOneField(Phase)

    details_confirmed = models.BooleanField(default=False)
    application_setup = models.BooleanField(default=False)
    announced_applications = models.BooleanField(default=False)
    invited_judges = models.BooleanField(default=False)
    announced_judging_open = models.BooleanField(default=False)
    selected_winners = models.BooleanField(default=False)

    def steps(self):

        return [self.details_confirmed,
                self.application_setup,
                self.announced_applications,
                self.invited_judged,
                self.announced_judging_open,
                self.selected_winners]

    def next_step_num(self):
        i = 0
        for step in self.steps():
            if not step:
                return i
            i += 1

        return i
        

class PhaseSetupStepsForm(ModelForm):

    class Meta:

        model = PhaseSetupSteps
        exclude = ('phase',)



#a collection of answers and files that a founder submits to a
#competition phase
class Pitch(models.Model):

    #creator & submitter of this pitch, who has applied to the
    #competition the pitch relates to
    #
    #TODO: DEPRECATED: will be replaced by self.team.owner
    owner = models.ForeignKey(Founder) 

    team = models.ForeignKey(Team, null=True)

    #the part of the contest this pitch is a submission to
    phase = models.ForeignKey(Phase, related_name="pitches")

    #has applicant chosen to publish it yet?
    is_draft = models.BooleanField(default=True)

    #timestamp for when this pitch was first submitted
    created = models.DateTimeField(auto_now_add=True, default=datetime.now)
    
    #timestamp for when this pitch was last modified
    last_modified = models.DateTimeField(auto_now=True, default=datetime.now)

    order = models.IntegerField(default=0)


    class Meta:
        ordering = ['order']


    def created_ms(self):

        return int(time.mktime(self.created.timetuple())*1000)


    def num_times_judged(self):
        print 'num times judged: %s, %s' % (len(self.judgements.all()), self.judgements.all())        
        return len(self.judgements.all())


    def average_score(self):

        total_score = 0
        num_pitches = self.judgements.count()

        for judged_pitch in self.judgements.all():
            total_score = total_score + judged_pitch.score()

        try: return float(total_score) / num_pitches
        except: return 0


    #who is pitching this idea?
    def team_name(self):

        if self.team and self.team.name:
            return self.team.name

        else:
            num = self.phase.pitches.all().index(self)
            return "Team %s" % num


    def __unicode__(self):

        return 'pitch (id=%s) for (owner=%s)' % (self.pk, self.owner)



#details about all the questions a founder needs to answer to
#apply to the contest. 
class PitchQuestion(models.Model):

    #ordering on admin panel and application form
    order = models.DecimalField(max_digits=4, decimal_places=2, default=1)

    #phase of the contest wanting this Q answered
    phase = models.ForeignKey(Phase) 

    #instructions for the user
    prompt = models.CharField(max_length=1000, default="", blank=True)

    #string of choices delimited with newlines. no choices means it's a
    #free answer text field. 1 choice is invalid. 2 choices of "True\nFalse"
    #is a boolean checkbox. 2-4 choices are radio buttons. 5 or more is a dropdown.
    raw_choices = models.CharField(max_length=2000, default="", blank=True)

    #how big to make the text entry widget
    field_rows = models.IntegerField(default=6)

    #optional questions aren't displayed to judges when they're blank
    is_required = models.BooleanField(default=True)

    #if true, then users don't see the question. this is used when you want
    #judges to leave feedback in a way that's disconnected from a particular
    #question.
    is_hidden_from_applicants = models.BooleanField(default=False)

    #how many points this question can be worth if answered perfectly
    #if max_points == 0, then there is no numerical grading portion to this
    #question
    max_points = models.IntegerField(default=10)

    #if set to a non-blank string, informs judge what the points represent (ie 0 is bad, 5 is great!)
    judge_points_prompt = models.CharField(default="", max_length=140)

    #if set to a non-blank string, judge is asked to write freeform text as feedback
    judge_feedback_prompt = models.CharField(default="", max_length=140)


    class Meta:
        ordering = ['order']


    #return raw_choices as a split and stripped array of choices
    def choices(self):

        if not self.raw_choices or self.raw_choices == "":
            return None
        
        chunks = self.raw_choices.splitlines()

        trimmed_chunks = []
        for chunk in chunks:
            trimmed_chunks.append(chunk.strip())
        
        return trimmed_chunks


    def __unicode__(self):

        return self.prompt



#answer to a PitchQuestion
class PitchAnswer(models.Model):

    question = models.ForeignKey(PitchQuestion)
    pitch = models.ForeignKey(Pitch, related_name="answers")

    answer = models.CharField(max_length=2000)
    
    
    def __unicode__(self):

        return self.answer


#details about all the questions a founder needs to upload to
#apply to the contest. 
class PitchUpload(models.Model):

    phase = models.ForeignKey(Phase) #owner
    prompt = models.CharField(max_length=1000) #instructions for applicant

    class Meta:
        ordering = ['id']

    def __unicode__(self):

        return self.prompt



#stuff uploaded to satisfy a PitchUpload
class PitchFile(models.Model):

    upload = models.ForeignKey(PitchUpload)
    pitch = models.ForeignKey(Pitch, related_name="files")
    
    filename = models.CharField(max_length=200) #/random_string/uploaded_file_name.ext
    file_location = models.CharField(max_length=500) #absolute path of location on server file was uploaded to


    def is_image(self):

        extension = self.filename.split('.')[-1]
        print 'extension: %s' % extension
        images = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

        return string.lower(extension) in images


    def scribd(self):

        try:
            return self.scribd_file_data
        except:
            return None


    def url(self):

        return "%suploads/%s" % (MEDIA_URL, self.filename)

    def __unicode__(self):
        
        return str(self.filename.split('/')[-1])



#some extra metadata for embedding uploaded docs as Scribd objects
class ScribdFileData(models.Model):

    #PitchFile we have an embed for
    pitch_file = models.OneToOneField(PitchFile, related_name="scribd_file_data")

    #scribd stuff, sent in the response when we upload
    doc_id = models.CharField(max_length=100)
    access_key = models.CharField(max_length=100)
    secret_password = models.CharField(max_length=100)
    


#an arbitrary, user-definable question for requesting non-standard information
#about a founder in the application
class ExtraFounderQuestion(models.Model):

    prompt = models.CharField(max_length=1000)
    #string of choices delimited with newlines. no choices means it's a
    #free answer text field. 1 choice is invalid. 2 choices of "True\nFalse"
    #is a boolean checkbox. 2-4 choices are radio buttons. 5 or more is a dropdown.
    raw_choices = models.CharField(max_length=2000)


    #return raw_choices as a split and stripped array of choices
    def choices(self):
        
        chunks = raw_choices.split("\n")

        for chunk in chunks:
            chunk = chunk.trim()

        return chunks


    def __unicode__(self):

        return self.prompt



#answer to a custom ExtraFounderQuestion
class ExtraFounderInfo(models.Model):

    question = models.ForeignKey(ExtraFounderQuestion)
    founder = models.ForeignKey(Founder, related_name="extra_info")
    answer = models.CharField(max_length=5000)


    def __unicode__(self):
        return self.answer
    


