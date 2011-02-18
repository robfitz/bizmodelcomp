from django.http import HttpResponse
try: import simplejson
except ImportError: import json as simplejson

from competition.models import *


def eliminate_pitch(request, pitch_id):
    
    result = message = ""

    #exists?
    try:
        pitch = Pitch.objects.get(id=pitch_id)
    except:
        result = "failure"
        message = "Could not retrieve requested pitch"

    #permissions?
    if not request.user.is_authenticated or not pitch.phase.competition.owner == request.user:
        result = "failure"
        message = "No permissions for requested pitch"

    #advance to next
    else:
        pitch.result = "Eliminated"
        pitch.save()
        result = "success"
    
    obj = {"result": result, "message": message}
    json = simplejson.dumps(obj)
    return HttpResponse(json, mimetype="application/json")


def advance_pitch(request, pitch_id):
    
    result = message = ""

    #exists?
    try:
        pitch = Pitch.objects.get(id=pitch_id)
    except:
        result = "failure"
        message = "Could not retrieve requested pitch"

    #permissions?
    if not request.user.is_authenticated or not pitch.phase.competition.owner == request.user:
        result = "failure"
        message = "No permissions for requested pitch"

    #advance to next
    else:
        pitch.result = "Advancing"
        pitch.save()
        result = "success"
    
    obj = {"result": result, "message": message}
    json = simplejson.dumps(obj)
    return HttpResponse(json, mimetype="application/json")



 


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
