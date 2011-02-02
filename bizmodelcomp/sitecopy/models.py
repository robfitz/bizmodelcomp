from django.db import models
import markdown

from competition.models import Competition

class SiteCopy(models.Model):

    id = models.CharField(primary_key=True, max_length=30)
    text = models.CharField(max_length=20000) #markdown/html


    def html(self):

        return markdown.markdown(self.text)

    def __unicode__(self):

        return self.text

    

class Testimonial(models.Model):
    
    text = models.CharField(max_length=1000)
    thumb_url = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    author_url = models.CharField(max_length=200)


    def __unicode__(self):

        return self.text



#defaults & information about all the text an organizer can
#customize which their applicants & entrants will see
class CustomCopyTemplate(models.Model):

    title = models.CharField(max_length=140, unique=True)
    tooltip = models.CharField(max_length=500, blank=True)

    default_text = models.CharField(max_length=2000, blank=True)


    def __unicode__(self):

        return self.title



#copy that's shown for a single competition, based off the
#CustomCopyTemplate and potentially customized by the organizer
class CustomCopy(models.Model):

    competition = models.ForeignKey(Competition)

    title = models.CharField(max_length=140, blank=True)
    text = models.CharField(max_length=2000, blank=True)


    def __unicode__(self):

        return self.title
