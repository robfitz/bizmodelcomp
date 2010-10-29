from judge.models import *

from django.contrib import admin
from django import forms


##class SiteCopyForm(forms.ModelForm):
##
##    text = forms.CharField(widget=forms.Textarea)
##
##
##
##class SiteCopyAdmin(admin.ModelAdmin):
##    list_display = ('id',)
##    form = SiteCopyForm
##
##
##
##class TestimonialForm(forms.ModelForm):
##
##    text = forms.CharField(widget=forms.Textarea)
##
##
##
##class TestimonialAdmin(admin.ModelAdmin):
##
##    form = SiteCopyForm
##
##
##
##class CustomCopyForm(forms.ModelForm):
##
##    text = forms.CharField(widget=forms.Textarea)
##    
##class CustomCopyTemplateForm(forms.ModelForm):
##
##    tooltip = forms.CharField(widget=forms.Textarea)
##    default_text = forms.CharField(widget=forms.Textarea)
##
##class CustomCopyAdmin(admin.ModelAdmin):
##
##    form = CustomCopyForm
##    
##class CustomCopyTemplateAdmin(admin.ModelAdmin):
##
##    form = CustomCopyTemplateForm

admin.site.register(Judge)
admin.site.register(JudgeInvitation)
