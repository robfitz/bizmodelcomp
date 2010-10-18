from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


from bizmodelcomp.competition.models import *
from sitecopy.models import *



#main landing page. sell that service!
def index(request):

    copy = {}

    copy_objs = SiteCopy.objects.all()
    for c in copy_objs:
        #this clusterfuck is just meant to grab all the copy
        #beginning with "index_" and then use whatever comes
        #after the "_" as a key to display it in the template
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
            competition.save()

            #every competition is composed of at least one phase,
            #which is the container for all of our questions & uploads
            default_phase = Phase(competition=competition)
            default_phase.save()

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
    #TODO: support multiple phases
    phase = Phase.objects.filter(competition=competition)[0]

    if request.user != competition.owner:
        return HttpResponseRedirect("/accounts/no_permissions/")

    if request.method == "POST" and len(request.POST) > 0:

        #existing/edited questions are at old_question_prompt_[pk]
        #existing/edited uploads are at old_upload_prompt_[pk]
        #newly created ones are at question/upload_prompt_[unimportant_number]
        
        for key in request.POST:

            try:
                
                prompt = request.POST[key]
                
                if key.startswith('old_question_prompt_'):
                    #check if existing question has been edited
                    q = PitchQuestion.objects.get(pk=key[len('old_question_prompt_'):])
                    if len(prompt.strip()) == 0:
                        q.delete()
                    elif q.prompt != prompt:
                        q.prompt = prompt
                        q.save()
                                    
                elif key.startswith('old_upload_prompt_'):
                    #check if existing upload has been edited
                    u = PitchUpload.objects.get(pk=key[len('old_upload_prompt_'):])
                    if len(prompt.strip()) == 0:
                        u.delete()
                    elif u.prompt != prompt:
                        u.prompt = prompt
                        u.save()

                elif key.startswith('question_prompt_'):
                    print 'found question'
                    #create new question
                    if prompt and len(prompt.strip())>0:
                        print 'creating with prompt %s' % prompt
                        q = PitchQuestion(phase=phase,
                                        prompt=prompt)
                        q.save()
                        print 'saved'

                elif key.startswith('upload_prompt_'):
                    #create new upload
                    if prompt and len(prompt.strip()) > 0:
                        u = PitchUpload(phase=phase,
                                        prompt=prompt)
                        u.save()
                        
            except: pass
            
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

