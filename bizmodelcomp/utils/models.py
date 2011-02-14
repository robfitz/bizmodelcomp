from django.db import models



class Tag(models.Model):

    name = models.CharField(max_length=50)


    def __unicode__(self):

        return self.name



class PitchTag(models.Model):

    name = models.CharField(max_length=50)
    is_standard = models.BooleanField(default=False)


    def __unicode__(self):

        return u"%s" % self.name
