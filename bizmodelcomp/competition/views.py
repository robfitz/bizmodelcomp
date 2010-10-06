from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from competition.models import *
from sitecopy.models import *



#main landing page. sell that service!
def index(request):

    copy = {}

    copy_objs = SiteCopy.objects.all()
    for c in copy_objs:
        #this clusterfuck is just meant to grab all the copy
        #beginning with "index_" and then use whatever comes
        #after the "_" as a key to display it in the template,
        #allowing us to add new copy blocks w/out server reboot
        if c.id.startswith('index_'):
            copy[c.id[len('index_'):]] = c.text

    return render_to_response("competition/index.html", locals())



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



#if competition_id is none, then you are editing a new
#contest which should be created when the user saves
#the inputted details
@login_required
def edit_competition(request, competition_id=None):

    competition = None
    
    if request.method == "POST" and len(request.POST) > 0:

        if competition_id:
            competition = Competition.objects.get(pk=competition_id)
            #must own competition to edit it
            if request.user != competition.owner:
                return HttpResponseRedirect("/user/no_permissions/")

        else:
            #if logged in and creating new competition, then
            #guaranteed to own it already
            competition = Competition()
            competition.owner = request.user

        if request.POST["name"]:
            competition.name = request.POST["name"]

        if request.POST["website"]:
            competition.website = request.POST["website"]
            
        competition.save()

        #allow chaining together of setup steps by the templates
        try:
            next = request.POST["next"] + str(competition.id)
        except: next = "/dashboard/"

        return HttpResponseRedirect(next)

    elif competition_id:
        
        competition = Competition.objects.get(pk=competition_id)

    return render_to_response("competition/edit_competition.html", locals())



@login_required
def edit_application(request, competition_id):

    competition = Competition.objects.get(pk=competition_id)

    if request.user != competition.owner:
        return HttpResponseRedirect("/accounts/no_permissions/")

    if request.method == "POST" and len(request.POST) > 0:

        for key in request.POST:
            print key

        #TODO: drop old questions & uploads

        #set required uploads "upload_prompt_#"
        i = 0
        while i < 100: #completely arbitrary upper limit of 100 uploads
            try:
                prompt = request.POST["upload_prompt_" + str(i)]
                print 'found prompt for %s: %s' % (i, prompt)
                u = PitchUpload(competition=competition,
                                prompt=prompt)
                u.save()
            except: pass
            i = i + 1
            
        #set required questions/answers "question_prompt_#"
        i = 0
        while i < 1000: #arbitrary upper limit of 1000 questions
            try:
                prompt = request.POST["question_prompt_" + str(i)]
                q = PitchQuestion(competition=competition,
                                  prompt=prompt)
                q.save()
            except: pass
            i = i + 1

        #redirect to appropriate next page
        try: next = request.POST["next"] + str(competition.id)
        except: next = "/dashboard/"
        return HttpResponseRedirect(next)

    return render_to_response('competition/edit_application.html', locals())




@login_required
def edit_phases(request, competition_id):

    competition = Competition.objects.get(pk=competition_id)

    if request.user != competition.owner:
        return HttpResponseRedirect("/accounts/no_permissions/")

    if request.method == "POST" and len(request.POST) > 0:

        try:
            next = request.POST["next"] + str(competition.id)
        except: next = "/dashboard/"

        return HttpResponseRedirect(next)

    return render_to_response('competition/edit_phases.html', locals())




#gives organizer the javascript for installing contest widgets
#on their site, or also links to hosted pages if they prefer that
@login_required
def edit_application_widgets(request, competition_id):

    competition = Competition.objects.get(pk=competition_id)

    if request.user != competition.owner:
        return HttpResponseRedirect("/accounts/no_permissions/")

    #TODO: un-hardcode URL
    base_url = "http://localhost:8000"

    return render_to_response('competition/edit_application_widgets.html', locals())

