from bizmodelcomp.competition.models import *
from django.contrib import admin
from django import forms

from bizmodelcomp.emailhelper.models import *
from bizmodelcomp.userhelper.models import *
from bizmodelcomp.utils.models import *

##class QuestionInline(admin.TabularInline):
##    model = Question
##    extra = 5
##    fields = ['order', 'prompt', 'is_primary', 'is_multi_part', 'extra_help']
##
##
##class WorksheetForm(forms.ModelForm):
##    tooltip = forms.CharField(widget=forms.Textarea)
##class WorksheetAdmin(admin.ModelAdmin):
##    list_display = ('key', 'title', 'color')
##    list_editable =  ('title', 'color')
##    inlines = [QuestionInline]
##    form = WorksheetForm
##    
##class QuestionAdmin(admin.ModelAdmin):
##    list_display = ('prompt', 'worksheet')
##    #list_editable = ('field_rows', 'contact_tag')
##    #list_display_links = ('prompt',)
##    search_fields = ('prompt','worksheet')
##    list_filter = ('worksheet',)
##    #date_hierarchy = 'timestamp'
##    exclude = ('order',)
##    #fields = ('worksheet', 'prompt', 'details', 'field_rows')
##    #filter_horizontal = ('many_to_many_field',)
##    #raw_id_fields = ('extraInfo',)
##
##    def owner(self, model):
##        return model.worksheet.user
##
##class BlogPostForm(forms.ModelForm):
##    contents_markdown = forms.CharField(widget=forms.Textarea)
##
##class BlogPostAdmin(admin.ModelAdmin):
##    form = BlogPostForm
##
##class LongCopyForm(forms.ModelForm):
##    text = forms.CharField(widget=forms.Textarea)
##
##class MedCopyForm(forms.ModelForm):
##    text = forms.CharField(widget=forms.Textarea)
##
##class LongCopyAdmin(admin.ModelAdmin):
##    form = LongCopyForm
##
##class MedCopyAdmin(admin.ModelAdmin):
##    form = MedCopyForm
##
##class CanvasTemplateForm(forms.ModelForm):
##    details = forms.CharField(widget=forms.Textarea)
##class CanvasTemplateAdmin(admin.ModelAdmin):
##    form = CanvasTemplateForm
##
##class CanvasBlockForm(forms.ModelForm):
##    override_tooltip = forms.CharField(widget=forms.Textarea)
##class CanvasBlockAdmin(admin.ModelAdmin):
##    form = CanvasBlockForm


class CompetitionForm(forms.ModelForm):

    terms_of_service = forms.CharField(widget=forms.Textarea, required=False)


class CompetitionAdmin(admin.ModelAdmin):

    list_display = ('name', 'owner', 'hosted_url', 'current_phase', 'website')
    list_filter = ('owner',)
    form = CompetitionForm


class PitchQuestionForm(forms.ModelForm):

    raw_choices = forms.CharField(widget=forms.Textarea, required=False)

class PitchQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'prompt', 'field_rows', 'max_points', 'is_hidden_from_applicants', 'phase', 'max_answer_words')
    list_editable = ('order', 'prompt', 'field_rows', 'max_points', 'is_hidden_from_applicants', 'max_answer_words')
    list_filter = ('phase',)
    form = PitchQuestionForm

class PitchAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'team_name', 'team', 'phase', 'order', 'last_modified')
    list_editable = ('order',)
    list_filter = ('phase',)
    search_fields = ['team__name',]
    
class PitchUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'phase', 'prompt')
    list_filter = ('phase',)

class FounderAdmin (admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'email', 'applicant_type', 'location', 'institution',)
    list_display_links = ('name',)
    list_filter = ('institution',)
    
class ExtraFounderInfoAdmin (admin.ModelAdmin):
    list_display = ('id', 'question', 'founder', 'answer')

class PitchAnswerAdmin (admin.ModelAdmin):
    list_display = ('id', 'question', 'pitch', 'answer',)
    list_filter = ('pitch',)
    
class PitchFileAdmin (admin.ModelAdmin):
    list_display = ('id', 'upload', 'pitch', 'filename', 'file_location',)
    list_filter = ('pitch',)

class PhaseAdmin (admin.ModelAdmin):
    list_display = ('id', 'name', 'competition', 'pitch_type', 'deadline', 'is_judging_enabled',)
    list_display_links = ('name',)
    list_filter = ('competition',)
    
class TeamAdmin (admin.ModelAdmin):
    list_display = ('id', 'owner', 'name')
    
class Bulk_emailAdmin (admin.ModelAdmin):
    list_display = ('id', 'competition', 'phase', 'subject', 'tag', 'message_markdown', 'sent_on_date')
    list_filter = ('competition', 'phase',)


admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(ApplicationRequirements)

admin.site.register(Founder, FounderAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(ExtraFounderInfo, ExtraFounderInfoAdmin)

admin.site.register(Pitch, PitchAdmin)
admin.site.register(PitchQuestion, PitchQuestionAdmin)
admin.site.register(PitchUpload, PitchUploadAdmin)
admin.site.register(PitchAnswer, PitchAnswerAdmin)
admin.site.register(PitchFile, PitchFileAdmin)

admin.site.register(Bulk_email, Bulk_emailAdmin)
admin.site.register(Sub_val)
admin.site.register(Val)
admin.site.register(FailedNewsletterSubscription)
admin.site.register(NewsletterSubscription)
admin.site.register(NewsletterUnsubscription)

admin.site.register(VerificationKey)
admin.site.register(UserProfile)
##admin.site.register(Worksheet, WorksheetAdmin)

admin.site.register(Tag)
