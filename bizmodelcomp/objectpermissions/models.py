from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class ObjectPermissions(models.Model):

    user = models.ForeignKey(User)

    #judges can view certain applications.
    #founders can edit their own 
    can_view = models.BooleanField()
    
