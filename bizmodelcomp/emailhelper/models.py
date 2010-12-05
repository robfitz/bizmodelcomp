from django.db import models
from competition.models import *

from datetime import datetime


#
class Bulk_email(models.Model):

    #which competition this email was sent with regards to
    competition = models.ForeignKey(Competition)

    #if it refers to a specific phase (eg applications are open) then
    #this value is set. if it's generic for a competition (eg thanks
    #for applying) then this is null
    phase = models.ForeignKey(Phase, default=None, blank=True, null=True)

    #if this is the sort of email we only want to send once per comp/phase
    #pair, we can set a tag and reject identically tagged future mail
    tag = models.CharField(max_length=140, blank=True, null=True)

    subject = models.CharField(max_length=200)

    message_markdown = models.CharField(max_length=5000)

    timestamp = models.DateTimeField(default=datetime.now)

    #semicolon delimited list
from django.db import models
from competition.models import *

from datetime import datetime


#
class Bulk_email(models.Model):

    #which competition this email was sent with regards to
    competition = models.ForeignKey(Competition)

    #if it refers to a specific phase (eg applications are open) then
    #this value is set. if it's generic for a competition (eg thanks
    #for applying) then this is null
    phase = models.ForeignKey(Phase, default=None, blank=True, null=True)

    #if this is the sort of email we only want to send once per comp/phase
    #pair, we can set a tag and reject identically tagged future mail
    tag = models.CharField(max_length=140, blank=True, null=True)

    subject = models.CharField(max_length=200)

    message_markdown = models.CharField(max_length=5000)

    dummy = models.CharField(default="", max_length=1)

    #semicolon delimited list
    #TODO: there's probably a more efficient option than making this
    #a million characters long (4MB per object)
    recipient_founders = models.CharField(max_length=1000000, default="", blank=True, null=True)

    #if None, then this message hasn't been sent yet
    sent_on_date = models.DateTimeField(default=None, blank=True, null=True)


    def recipients(self):

        recipient_emails = self.recipient_founders.split(';')

        return recipient_emails


    def substitutions(self):

        subs = {}
        
        for sub_val in self.sub_val_set.all():
            
            subs[sub_val.key] = sub_val.vals()

        return subs



class Sub_val(models.Model):

    email = models.ForeignKey(Bulk_email)
    
    key = models.CharField(max_length=140)


    def vals(self):

        values = []

        for val in self.val_set.all():

            values.append(val.val);

        return values



class Val(models.Model):

    order = models.IntegerField()

    sub_val = models.ForeignKey(Sub_val)

    val = models.CharField(max_length=500)

    class Meta:
        ordering = ['order']

    #TODO: there's probably a more efficient option than making this
    #a million characters long (4MB per object)
    recipient_founders = models.CharField(max_length=1000000)

    #if None, then this message hasn't been sent yet
    sent_on_date = models.DateTimeField(default=None, blank=True, null=True)


    def recipients(self):

        recipient_emails = self.recipient_founders.split(';')

        return recipient_emails


    def substitutions(self):

        subs = {}
        
        for sub_val in self.sub_val_set.all():
            
            subs[sub_val.key] = sub_val.vals()

        return subs



class Sub_val(models.Model):

    email = models.ForeignKey(Bulk_email)
    
    key = models.CharField(max_length=140)


    def vals(self):

        values = []

        for val in self.val_set.all():

            values.append(val.val);

        return values



class Val(models.Model):

    order = models.IntegerField()

    sub_val = models.ForeignKey(Sub_val)

    val = models.CharField(max_length=500)

    class Meta:
        ordering = ['order']

