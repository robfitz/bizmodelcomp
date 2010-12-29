from django.forms import ModelForm
from django import forms

from emailhelper.models import Bulk_email



class BulkEmailForm(ModelForm):

    message_markdown = forms.CharField(widget=forms.Textarea, label="Message text")

    tag = forms.CharField(label="Descriptive tag")


    class Meta:

        model = Bulk_email
        fields = ('tag', 'subject', 'message_markdown')

    
