from bizmodelcomp.competition.models import *
from django.contrib import admin
from django import forms

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

    

admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Founder)
admin.site.register(ExtraFounderInfo)
admin.site.register(Business)

##admin.site.register(Worksheet, WorksheetAdmin)
