from django.db import models
import markdown



class SiteCopy(models.Model):

    id = models.CharField(primary_key=True, max_length=30)
    text = models.CharField(max_length=2000) #markdown/html


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
