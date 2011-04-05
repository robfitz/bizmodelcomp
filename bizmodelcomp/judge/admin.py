from judge.models import *

from django.contrib import admin
from django import forms


class JudgeInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'this_phase_only', 'competition', 'email', 'has_received_invite_email', 'user')
    list_filter = ('competition',)
    
class JudgePitchAdmin(admin.ModelAdmin):
    list_display = ('id', 'pitch', 'judge', 'feedback', 'overall_score', 'max_overall_score', 'timestamp', 'score')
    list_filter = ('pitch', 'judge')
    
class JudgeAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'judged_pitch', 'answer', 'criteria', 'score', 'feedback')
    list_filter = ('judged_pitch',)
    
class JudgingCriteriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'phase', 'order', 'prompt', 'max_points', 'is_text_feedback', 'is_feedback_sent_to_applicants', 'scoring_tooltip')
    list_editable = ('order',)
    list_filter = ('phase',)
    

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

admin.site.register(JudgeInvitation, JudgeInvitationAdmin)
admin.site.register(JudgedPitch, JudgePitchAdmin)
admin.site.register(JudgedAnswer, JudgeAnswerAdmin)
admin.site.register(JudgingCriteria, JudgingCriteriaAdmin)
