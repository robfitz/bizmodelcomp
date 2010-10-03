from django.http import HttpResponse
import simplejson

from competition.models import *
    


##def apply_to_competition(request):
##
##    result = "failure"
##
##    if request.method == "POST" and len(request.POST) > 0):
##        try:
##            competition_id = request.POST["competition"]
##            competition = Competition.objects.get(pk=competition_id)
##        except:
##            pass
##
##        if competition:
##
##            founder = Founder()
##            
##            for keys in request.POST:
##
##                #set standard/required values
##                if key in dir(founder):
##                    setattr(founder, key, request.POST[key])
##
##            founder.save()
##        
##
##    obj = {"result":result}
##    json = simplejson.dumps(obj)
##
##    return HttpResponse(json, mimetype="application/json")
