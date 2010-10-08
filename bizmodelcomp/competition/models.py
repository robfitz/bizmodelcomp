from django.db import models
from django.contrib.auth.models import User




#guy with a business model who is developing it, applying
#for contests, or getting feedback from peers
class Founder(models.Model):

    name = models.CharField(max_length=500) #don't use first/last/etc for multi-cultural reasons
    email = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)

    birth = models.IntegerField(blank=True, null=True) #representation of a datetime


    #returns the set of ExtraFounderInfos attached to this Founder as
    #a dictionary of question:answer pairs 
    def extra(self):
        dictionary = {}
        for info in self.extra_info.all():
           dictionary[info.question.prompt] = info.answer
        return dictionary
        

    def __unicode__(self):

        return self.name



#a business model competition
class Competition(models.Model):

    name = models.CharField(max_length=500, blank=True, default="")
    website =  models.CharField(max_length=500, blank=True, default="")

    owner = models.ForeignKey(User) #single owner who can delete it
    applicants = models.ManyToManyField(Founder, related_name="competitions") #info about peeps entered in contest


    def __unicode__(self):

        return self.name



#a subset of a competition, which involves applicants submitting
#some form of pitch which is then judged
class Phase(models.Model):

    competition = models.ForeignKey(Competition)
    name = models.CharField(max_length=500, blank=True, default="")


    def questions(self):

        return self.pitchquestion_set.all()


    def uploads(self):

        return self.pitchupload_set.all()
    
    



#a collection of answers and files that a founder submits to a
#competition phase
class Pitch(models.Model):

    #creator & submitter of this pitch, who has applied to the
    #competition the pitch relates to
    owner = models.ForeignKey(Founder) 

    #the part of the contest this pitch is a submission to
    phase = models.ForeignKey(Phase)



#details about all the questions a founder needs to answer to
#apply to the contest. 
class PitchQuestion(models.Model):

    phase = models.ForeignKey(Phase) #piece of the contest wanting this Q answered
    prompt = models.CharField(max_length=1000) #instructions for applicant

    #string of choices delimited with newlines. no choices means it's a
    #free answer text field. 1 choice is invalid. 2 choices of "True\nFalse"
    #is a boolean checkbox. 2-4 choices are radio buttons. 5 or more is a dropdown.
    raw_choices = models.CharField(max_length=2000, null=True, blank=True)


    #return raw_choices as a split and stripped array of choices
    def choices(self):
        
        chunks = raw_choices.split("\n")

        for chunk in chunks: chunk = chunk.trim()
        
        return chunks


    def __unicode__(self):

        return self.prompt



#answer to a PitchQuestion
class PitchAnswer(models.Model):

    question = models.ForeignKey(PitchQuestion)
    pitch = models.ForeignKey(Pitch)

    answer = models.CharField(max_length=2000)



#details about all the questions a founder needs to upload to
#apply to the contest. 
class PitchUpload(models.Model):

    phase = models.ForeignKey(Phase) #owner
    prompt = models.CharField(max_length=1000) #instructions for applicant


    def __unicode__(self):

        return self.prompt



#stuff uploaded to satisfy a PitchUpload
class PitchFile(models.Model):

    upload = models.ForeignKey(PitchUpload)
    pitch = models.ForeignKey(Pitch)
    
    filename = models.CharField(max_length=200)


    def __unicode__(self):
        
        return self.filename

    

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
    


