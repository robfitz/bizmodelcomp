from django.db import models
from competition.models import *
import string

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

    #if None, then this message hasn't been sent yet
    sent_on_date = models.DateTimeField(default=None, blank=True, null=True)


    def preview_messages(self):

        subs = {}
        for sub_val in Sub_val.objects.filter(email=self): 
            subs[sub_val.key] = []

        messages = []
        val = ""

        for i in range(0, len(self.recipients())):

            message = {}
            message["to_email"] = self.recipients()[i]
            message["body"] = self.message_markdown

            #TODO: use string.parse(format_string) instead of this manual replacing
            for sub_val in Sub_val.objects.filter(email=self):
                print 'looking @ sub_val: %s' % sub_val.key
                try:
                    val = Val.objects.get(order=i, sub_val=sub_val).val
                    print '    found val: %s' % val
                except: val = ""

                subs[sub_val.key].append(val)

                message["body"] = string.replace(message["body"], sub_val.key, val)
                print '    replaced in body'
                print message["body"]
                print ''
                print ''
        

            messages.append(message) 

        return messages



    def recipients(self):

        recipient_emails = []

        for address in self.recipient_addresses.all():
            recipient_emails.append(address.address)

        return recipient_emails


    def substitutions(self):

        subs = {}
        
        for sub_val in self.sub_val_set.all():
            
            subs[sub_val.key] = sub_val.vals()

        return subs



class Email_address(models.Model):

    order = models.IntegerField()

    bulk_email = models.ForeignKey(Bulk_email, related_name="recipient_addresses")

    address = models.CharField(max_length=140)

    #optional link to a user. set it if it's relevant just so we
    #have a bit of extra info in case people's email or whatever changes.
    user = models.ForeignKey(User, default=None, blank=True, null=True)

    

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

    val = models.CharField(max_length=10000)

    class Meta:

        ordering = ['order']
