from bizmodelcomp.sitecopy.models import *

from django.contrib import admin
from django import forms


class SiteCopyForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea)



class SiteCopyAdmin(admin.ModelAdmin):

    form = SiteCopyForm



class TestimonialForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea)



class TestimonialAdmin(admin.ModelAdmin):

    form = SiteCopyForm



    


admin.site.register(SiteCopy, SiteCopyAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
