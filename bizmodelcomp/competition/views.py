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



def create_new_comp_for_user(user):
	key = None
	while True: 
		#find a unique url for the competition
		key = rand_key(6)
		try: 	Competition.objects.get(hosted_url=key)
		except:	break
			
	competition = Competition(owner=user, hosted_url=key)
	competition.save()
	competition.current_phase = Phase(competition=competition)
	competition.current_phase.save()
	competition.save()

       	if not user.get_profile():
	    #ensure old accounts have a profile
	    profile = UserProfile(user=request.user)
	    profile.selected_competition = competition
	    profile.save()

	return competition



#if competition_id is none, then you are editing a new
#contest which should be created when the user saves
#the inputted details
@login_required
def edit_competition(request, competition_id=None):

    alert = ""
    competition = None
    
    if request.method == "POST" and len(request.POST) > 0:

        if competition_id:
	    print 'competition id: %s' % competition_id
            competition = Competition.objects.get(pk=competition_id)
            #must own competition to edit it
            if request.user != competition.owner:
                return HttpResponseRedirect("/user/no_permissions/")

        else:
            competition = create_new_comp_for_user(request.user)


        competition.name = request.POST["name"]
        competition.website = request.POST["website"]
        competition.save()

	competition.hosted_url = request.POST["hosted_url"]
        
	try:
            competition.save()
	except:
	    alert = "The competition URL \"%s\" is already taken. Try using a different one." % request.POST.get("hosted_url")

        #allow chaining together of setup steps by the templates
        try:
            next = request.POST["next"] + str(competition.id)
        except: next = "/dashboard/"

        if not alert:
	    #if there's an error alert, don't go on to the next step
	    return HttpResponseRedirect(next)

    elif competition_id:
        
        competition = Competition.objects.get(pk=competition_id)

    return render_to_response("competition/edit_competition.html", locals())



@login_required
def edit_application(request, phase_id):

    #competition = Competition.objects.get(pk=competition_id)
    phase = Phase.objects.get(id=phase_id)

    if request.user != phase.competition.owner:
	print 'request.user: %s, phase id: %s, comp owner: %s' % (request.user, phase_id, phase.competition.owner)
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
        try: next = request.POST["next"] + str(phase.competition.id)
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

    base_url = "http://%s" % request.get_host()

    return render_to_response('competition/edit_application_widgets.html', locals())

