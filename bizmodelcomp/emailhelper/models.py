from django.db import models
from competition.models import Founder



#
class Bulk_email(models.Model):

    subject = models.CharField(max_length=200)

    message_markdown = models.CharField(max_length=5000)

    #semicolon delimited list
    recipient_founders = models.CharField(max_length=10000)

    #if None, then this message hasn't been sent yet
    sent_on_date = models.DateTimeField(default=None, blank=True, null=True)


    def recipients(self):

##        recipient_emails = []
##
##        for recipient in self.recipient_founders.all():
##
##            recipient_emails.push(recipient.email)

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

    sub_val = models.ForeignKey(Sub_val)

    val = models.CharField(max_length=500)
