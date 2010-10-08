from django.db import models
from bizmodelcomp.competition import Founder


#randomized url to [.key] provides equivalent
#permissions to logging in with a username and password.
#identity should be verified by asking them to type in
#their email (url + email ~= email + password)
class RandomFounderUrl(models.Model):

    #randomized url key that gets shipped to a new user's
    #email if they don't feel like making a username/pw
    key = models.CharField(primary_key=True)

    #person who is logging in
    founder = models.OneToOneField(Founder)

    #when someone validates w/ email, we log them in so
    #we can get at the rest of the info for the session
    temp_password = models.CharField()
