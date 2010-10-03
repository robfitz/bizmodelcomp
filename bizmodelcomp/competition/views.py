from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from competition.models import *
from sitecopy.models import *
    


def index(request):

    try: benefits = SiteCopy.objects.get(id='benefits')
    except: pass
    
    try: roi = SiteCopy.objects.get(id='roi')
    except: pass
        
    try: tour = SiteCopy.objects.get(id='tour')
    except: pass

    return render_to_response("competition/index.html", locals())



@login_required
def dashboard(request):

    competitions = Competition.objects.all()

    return render_to_response("competition/dashboard.html", locals())



#view list of applicants, sort & manipulate them
@login_required
def manage_applicants(request, competition_id):

    competition = Competition.objects.get(pk=competition_id)
    print competition.applicants.all()

    return render_to_response("competition/manage_applicants.html", locals())


#if competition_id is none, then you are editing a new
#contest which should be created when the user saves
#the inputted details
@login_required
def edit_competition(request, competition_id=None):

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/user/no_permissions/")

    competition = None
    
    if request.method == "POST" and len(request.POST) > 0:

        if competition_id:
            competition = Competition.objects.get(pk=competition_id)

        else:
            competition = Competition()
            competition.owner = request.user

        if request.POST["name"]:
            competition.name = request.POST["name"]

        if request.POST["website"]:
            competition.website = request.POST["website"]
            
        competition.save()

        return HttpResponseRedirect("/dashboard")

    elif competition_id:

        competition = Competition.objects.get(pk=competition_id)

    return render_to_response("competition/edit_competition.html", locals())

