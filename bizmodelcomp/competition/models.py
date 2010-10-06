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
    applicants = models.ManyToManyField(Founder) #info about peeps entered in contest


    def __unicode__(self):

        return self.name



#details about all the questions a founder needs to answer to
#apply to the contest. 
class PitchQuestions(models.Model):

    competition = models.OneToOneField(Competition) #owner
    prompt = models.CharField(max_length=1000) #instructions for applicant

    #string of choices delimited with newlines. no choices means it's a
    #free answer text field. 1 choice is invalid. 2 choices of "True\nFalse"
    #is a boolean checkbox. 2-4 choices are radio buttons. 5 or more is a dropdown.
    raw_choices = models.CharField(max_length=2000)


    #return raw_choices as a split and stripped array of choices
    def choices(self):
        
        chunks = raw_choices.split("\n")

        for chunk in chunks: chunk = chunk.trim()
        
        return chunks


    def __unicode__(self):

        return self.prompt


#details about all the questions a founder needs to upload to
#apply to the contest. 
class PitchUpload(models.Model):

    competition = models.OneToOneField(Competition) #owner
    prompt = models.CharField(max_length=1000) #instructions for applicant

    def __unicode__(self):

        return self.prompt


#an arbitrary, user-definable question for requesting non-standard information
#about a founder in the application
class ExtraQuestion(models.Model):

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



#answer to a custom ExtraQuestion
class ExtraFounderInfo(models.Model):

    question = models.ForeignKey(ExtraQuestion)
    founder = models.ForeignKey(Founder, related_name="extra_info")
    answer = models.CharField(max_length=5000)


    def __unicode__(self):
        return self.answer
    


#the thing a founder makes which is then pitched to
#competitions
class Business(models.Model):

    pass



