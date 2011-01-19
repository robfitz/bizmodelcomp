from bizmodelcomp.competition.models import *
from django.contrib import admin
from django import forms

from bizmodelcomp.emailhelper.models import *
from bizmodelcomp.userhelper.models import *
from bizmodelcomp.blog.models import *

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



class CompetitionAdmin(admin.ModelAdmin):

    list_display = ('name', 'owner', 'website')


class PitchQuestionForm(forms.ModelForm):

    raw_choices = forms.CharField(widget=forms.Textarea, required=False)

class PitchQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'prompt', 'field_rows', 'max_points', 'is_hidden_from_applicants', 'phase')
    list_editable = ('order', 'prompt', 'field_rows', 'max_points', 'is_hidden_from_applicants',)
    list_filter = ('phase',)
    form = PitchQuestionForm



class PitchAdmin(admin.ModelAdmin):
    list_display = ('id', 'team_name', 'phase', 'order')
    list_editable = ('order',)
    list_filter = ('phase',)



admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Phase)

admin.site.register(Founder)
admin.site.register(Team)
admin.site.register(ExtraFounderInfo)

admin.site.register(Pitch, PitchAdmin)
admin.site.register(PitchQuestion, PitchQuestionAdmin)
admin.site.register(PitchUpload)
admin.site.register(PitchAnswer)
admin.site.register(PitchFile)

admin.site.register(Bulk_email)
admin.site.register(Sub_val)
admin.site.register(Val)

admin.site.register(VerificationKey)
admin.site.register(UserProfile)
##admin.site.register(Worksheet, WorksheetAdmin)

admin.site.register(BlogPost)
