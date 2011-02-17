from django.db import models
from django.contrib.auth.models import User


class VerificationKey(models.Model):

    key = models.CharField(max_length=20, primary_key=True)

    user = models.ForeignKey(User, null=True)

    email = models.CharField(max_length=140, unique=True, null=True)

    #can get pre-verified before registration by clicking
    #on a link that is sent straight to your supplied inbox
    is_verified = models.BooleanField(default=False)



class UserProfile(models.Model):

    user = models.OneToOneField(User, null=True)


    #best guess at an appropriate display name
    def name(self):

        try:
            if self.user.first_name:
                return self.user.first_name

            else:
                return self.user.email.split('@')[0]

        except:
            return "No name!"
