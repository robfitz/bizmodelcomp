from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from bizmodelcomp.competition.models import *



#view list of applicants, sort & manipulate them
@login_required
def list_applicants(request, competition_id):

    #is comp valid?
    try:
        competition = Competition.objects.get(pk=competition_id)
    except:
        return HttpResponseRedirect("/no_permissions/")

    #is organizer?
    if not competition.owner == request.user:
        return HttpResponseRedirect("/no_permissions/")
    
    return render_to_response("dashboard/list_applicants.html", locals())



#view list of pitches, sort & manipulate them
@login_required
def list_pitches(request, competition_id, phase_id):

    #are comp & phase valid?
    try:
        competition = Competition.objects.get(id=competition_id)
        phase = Phase.objects.filter(competition=competition).get(id=phase_id)
    except:
        return HttpResponseRedirect("/no_permissions/")

    #is organizer?
    if not competition.owner == request.user:
        return HttpResponseRedirect("/no_permissions/")
    
    return render_to_response("dashboard/list_pitches.html", locals())



#view & manage your competitions
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

