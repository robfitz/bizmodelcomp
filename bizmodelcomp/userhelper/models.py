from django.db import models
from django.contrib.auth.models import User

from competition.models import Competition

class VerificationKey(models.Model):

    key = models.CharField(max_length=20, primary_key=True)

    user = models.ForeignKey(User, unique=True, null=True)

    email = models.CharField(max_length=140, unique=True, null=True)

    #can get pre-verified before registration by clicking
    #on a link that is sent straight to your supplied inbox
    is_verified = models.BooleanField(default=False)



class UserProfile(models.Model):

    selected_competition = models.ForeignKey(Competition, blank=True, null=True)


    def competition(self):

        if self.selected_competition:
	    return self.selected_competition
        
        else:
	    
	    comps = Competition.objects.get(owner=self.user)
	    if len(comps) > 0:
	        return comps[0]

	return None
