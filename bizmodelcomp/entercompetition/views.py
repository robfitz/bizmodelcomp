from bizmodelcomp.competition.models import *
from django.shortcuts import render_to_response
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect

from random import choice
import string
import os

from bizmodelcomp.settings import MEDIA_ROOT
from sitecopy.util import get_custom_copy



def recover_application(request):
    #TODO:
    pass


#helper
def get_founder(request):

    founder = None

    #figure out which user this is for
    if 'f' in request.GET:
        #using an anon link
        rand_key = request.GET.get("f")
        print rand_key
        key = AnonymousFounderKey.objects.get(key=rand_key)
        print key
        founder = key.founder
        

        if request.user.is_authenticated and founder.user != request.user:
            #start freaking out, logged in user is using someone else's key
            #possibly merge accounts, possibly logout, possibly refuse permissions
            print "TODO: entercompetition.views.get_founder(): conflicting login & anon key"

    elif request.session.get('founder_key', False):

        #not logged in, but key is in session
        rand_key = request.session.get('founder_key')
        key = AnonymousFounderKey.objects.get(key=rand_key)
        founder = key.founder
                 
    elif request.user.is_authenticated():
        #already logged in, that's easy
        try:
            founder = Founder.objects.get(user=request.user)
        except:
            print "TODO: entercompetition.views.get_founder(): unhandled bad login case"

    return founder



def submit_pitch(request, competition_url, phase_id=None):

    competition = Competition.objects.get(hosted_url=competition_url)
    phase = None
    pitch = None

    founder = get_founder(request)

    if not founder:
        #we don't know who is applying, so we'll display an extra email field
        #on the application form. This covers two cases:
        #
        #1) we've imported applicants from an external source (like a csv) so
        #   we have their data stored as ExternalFounder objects. If they enter
        #   an email that is in an ExternalFounder, we merge the data.
        #
        #2) they've snuck directly to this URL. if we have no record of the email
        #   submitted, we'll then show them the application widget to collect rest
        #   of their personal info.
        pass
    
    if phase_id: phase = Phase.objects.get(pk=phase_id) #requested specific phase
    else: phase = competition.phases()[0] #use default (first) phase

    try: pitch = Pitch.objects.filter(owner=founder).get(phase=phase)
    except: pass

    if request.method == "POST" and len(request.POST) > 0:

        if not founder:
            try:
                #this field should be present in the form whenever founder==None
                email = request.POST["email"]

                #do we recognize that email?
                mystery_founder = None
                try:
                    mystery_founder = Founder.objects.get(email=email)
                    if mystery_founder.require_authentication:
                        #TODO: need to authenticate via email URL.
                        return False
                    else:
                        #no auth needed, so just save it as a pitch

                        #log in to session
                        request.session['founder_key'] = mystery_founder.anon_key()
                        
                        #now that there's a pitch, we want them to identify
                        #themselves from now on
                        mystery_founder.require_authentication = True
                        mystery_founder.save()

                except:
                    #we don't have a founder on record who matches that email

                    #TODO: create a skeleton Founder object & redirect them to
                    #application form to fill in the rest of the details
                    pass
                
                
            except:
                #TODO: if founder is None and there's on POST.email we're
                #in real trouble. do something with this.
                return False
            

        if not pitch:
            #don't create pitch until someone submits the form
            pitch = Pitch(owner=founder,
                          phase=phase)
            pitch.save()


        if "is_draft" in request.POST:
            #this key is not always present
            pitch.is_draft = (request.POST["is_draft"] == "True")
            pitch.save()
            

        #deal w/ saved answers
        for key in request.POST:

            if key.startswith("question_"):
                try:
                    question_pk = key[len("question_"):]
                    question = PitchQuestion.objects.get(pk=question_pk)

                    answer = None
                    try:
                        #existing answer?
                        answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)
                        answer.answer=request.POST[key]
                    except:                    
                        answer = PitchAnswer(question=question,
                                             pitch=pitch,
                                             answer=request.POST[key])
                    answer.save()

                except: pass

        #deal w/uploads
        for file in request.FILES:
            upload_pk = file[len("upload_"):]
            upload = PitchUpload.objects.get(pk=upload_pk)
            handle_uploaded_file(request, request.FILES[file], upload, pitch)


    copy = get_custom_copy('thanks for applying', competition)
    return render_to_response('entercompetition/submitted_pitch.html', locals())



def edit_pitch(request, competition_url, phase_id=None):

    competition = Competition.objects.get(hosted_url=competition_url)
    phase = None
    pitch = None

    founder = get_founder(request)

    if not founder:
        #we don't know who is applying, so we'll display an extra email field
        #on the application form. This covers two cases:
        #
        #1) we've imported applicants from an external source (like a csv) so
        #   we have their data stored as ExternalFounder objects. If they enter
        #   an email that is in an ExternalFounder, we merge the data.
        #
        #2) they've snuck directly to this URL. if we have no record of the email
        #   submitted, we'll then show them the application widget to collect rest
        #   of the personal info.
        pass

    if phase_id: phase = Phase.objects.get(pk=phase_id) #requested specific phase
    else: phase = competition.phases()[0] #use default (first) phase

    try: pitch = Pitch.objects.filter(owner=founder).get(phase=phase)
    except: pitch = None
        
    questions = phase.questions()
    uploads = phase.uploads()
    
    for question in questions:
        #render existing answers
        try: question.answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)
        except: question.answer = ""

    for upload in uploads:
        #render existing uploads
        try: upload.file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
        except: upload.file = None

    return render_to_response('entercompetition/pitch_form.html', locals())



def handle_uploaded_file(request, f, upload, pitch):

    upload_path = '%suploads/' % MEDIA_ROOT
    file_name = ""
    
    #add to a random directory to avoid collisions
    rand_folder = ''.join([choice(string.letters+string.digits) for i in range(20)])
    upload_path = "%s%s/" % (upload_path, rand_folder)
    download_path = "%s/" % rand_folder

    if not os.path.isdir(upload_path):
        os.mkdir(upload_path)

    #preserve filename where possible
    if f.name:
        #name same as original file, in random folder
        upload_path = "%s%s" % (upload_path, f.name)
        file_name = "%s/%s" % (rand_folder, f.name)
    else:
        #random name
        upload_path = "%s%s.bmc" % (upload_path, rand_folder)
        file_name = "%s/%s.bmc" % (rand_folder, rand_folder)

    print 'upload path: %s' % upload_path
    print 'file_name: %s' % file_name

    destination = open(upload_path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

    pitch_file = None
    try:
        pitch_file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
        pitch_file.file_location = upload_path
        pitch_file.filename = file_name
    except:
        pitch_file = PitchFile(upload=upload,
                               file_location=upload_path,
                               filename=file_name,
                               pitch=pitch)
    pitch_file.save()
    


#a hosted microsite to accept contest applications
def applicationMicrosite(request, competition_url):

    #TODO: un-hardcode URL
    base_url = "http://%s" % request.get_host()
    
    competition = Competition.objects.get(hosted_url=competition_url)

    return render_to_response('entercompetition/application_microsite.html', locals())



#creates some slightly customized javascript to load the appropriate
#contest widget into the admin's page
def applicationWidget(request, competition_url):
    callback_function = "bmc_callback"

    form = """\
<form id="bmc_form" action="." method="GET" onsubmit="return apply(\\'%s\\')">\
    <p>\
    Name<br/>\
    <input type="text" name="name" id="bmc_field" />\
    </p>\
\
    <p>\
    Email<br/>\
    <input type="text" name="email" id="bmc_field" />\
    </p>\
\
    <p>\
    MM/DD/YYYY Birthday<br/>\
    <input type="text" name="month" id="bmc_field" size="2" max="2" />\
    <input type="text" name="day" id="bmc_field" size="2" max="2" />\
    <input type="text" name="year" id="bmc_field" size="4" max="4" />    \
    </p>\
\
    <input type="hidden" name="callback_function" id="bmc_field" value="%s"/>\
    <input type="submit" value="Register for competition" />\
</form>\
""" % (competition_url, callback_function)

    template = loader.get_template("entercompetition/widget.js")
    rendered = template.render(Context(locals()))

    return HttpResponse(rendered, mimetype="application/javascript")



#accepts a brand new application for the contest, which makes a
#Founder object to represent the applicant and hooks them into
#the contest to receive alerts and submit their full pitch
def applyToCompetition(request, competition_url):

    competition = Competition.objects.get(hosted_url=competition_url)
    callback_function = "bmc_callback" #a probably correct default

    if competition and request.method == "GET" and len(request.GET) > 0:

        founder = Founder()
        
        for key in request.GET:
            
            print "%s: %s" % (key, request.GET[key])

            #set standard/required values
            if key in request.GET:
                try: setattr(founder, key, request.GET[key])
                except: pass

        try: callback_function = request.GET["callback_function"]
        except: pass

        founder.save()
        competition.applicants.add(founder)

        try:
            rand = ''.join([choice(string.letters+string.digits) for i in range(12)])
            anon = AnonymousFounderKey(key=rand,
                                       founder=founder)
            anon.save()
        except:
            print "Unexpected error:", sys.exc_info()[0]

        message = """<p>\
You're registered for the\ competition and will receive email updates as the deadline approaches.\
</p>\
<p style='font-size:18px;'>\
<a href='/apply/pitch/%s/?f=%s'>Go fill out the application form right now</a>\
</p>\
""" % (competition_url, anon.key)

    else:
        message = "Sorry, the application service is temporarily down. Please try again soon."

    params = '{ "message": "%s"}' % message
    response = "%s( %s )" % (callback_function, params)

    print 'RESPONSE: %s' % response

    return HttpResponse(response, mimetype="application/javascript")


