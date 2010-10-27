from bizmodelcomp.competition.models import *
from django.shortcuts import render_to_response
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect

from random import choice
import string
import os

from bizmodelcomp.settings import MEDIA_ROOT
from sitecopy.models import SiteCopy
from sitecopy.util import get_custom_copy
from emailhelper.util import send_email



#user has claimed to have already submitted an application, so we're
#going to give them some extra info about how to get back to their old
#version and send them a reminder email if needed
def recover_application(request, competition_url):

    competition = Competition.objects.get(hosted_url=competition_url)

    intro = SiteCopy.objects.get(id='recover_application_intro')
    security = SiteCopy.objects.get(id='recover_application_security')

    application_url = "/apply/pitch/%s/" % competition.hosted_url
    cancel = "<a href='%s'>Cancel and return to a new application</a>" % application_url

    get_email = ""
    if request.method == "GET":
        get_email = request.GET.get("e")
        if not get_email:
            get_email = ""
        
    if request.method == "POST" and len(request.POST) > 0:

        try:
            #look for a founder w/ the matching email, and send them a note
            email = request.POST["email"]
            matching_founder = Founder.objects.get(email=email)

            subject = "Your application to %s" % competition.name

            application_url = request.build_absolute_uri("/pitch/apply/%s/?f=%s" % (competition.hosted_url, matching_founder.anon_key()))
            
            message = """Click here to load & edit your application to %s:

%s""" % (competition.name, application_url)
            
            send_email(subject, message, email)

            return HttpResponseRedirect('/apply/sent_reminder/')
            
        except:
            #couldn't find a matching founder. tell person to apply now or re-type
            application_url = "/apply/pitch/%s/" % competition.hosted_url
            alert = """We couldn't find a matching email on file. If you might have registered with a different email, you can try that here.

Otherwise, <a href="%s">click here to go back to your new application</a>.""" % application_url
    
    return render_to_response('entercompetition/recover_application.html', locals())



def sent_reminder(request):

    copy = """We've sent an email with a login link to the address you just submitted. After clicking that link, you'll be asked to type in your email one last time and then you'll [finally] see your application.

Jumping through these hoops helps ensure your pitch stays private -- sorry for the hassle!"""

    return render_to_response('entercompetition/sent_reminder.html', locals())


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
    
    is_first_pitch = False
    #if true, user registered via data import rather than through widget,
    #so we haven't yet sent them a recovery email
    is_new_founder = False 

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
                        print 'mystery founder with no auth needed'

                        #log in to session
                        request.session['founder_key'] = mystery_founder.anon_key()
                        print 'set anon key'
                        
                        #now that there's a pitch, we want them to identify
                        #themselves from now on
                        mystery_founder.require_authentication = True
                        mystery_founder.save()
                        
                        founder = mystery_founder

                        is_new_founder = True
                        print 'set external = true'
                    
                except:
                    #we don't have a founder on record who matches that email

                    #TODO: create a skeleton Founder object & redirect them to
                    #application form to fill in the rest of the details

                    #create founder
                    founder = Founder(email=email)
                    founder.save()
                    is_new_founder = True

                    #log in
                    request.session['founder_key'] = founder.anon_key()

            except:
                #TODO: if founder is None and there's no POST.email we're
                #in real trouble. do something with this.
                return False
            

        if not pitch:
            #don't create pitch until someone submits the form
            print 'pitch = NOne, creating new'
            pitch = Pitch(owner=founder,
                          phase=phase)
            pitch.save()
            #can show different success message on first submission
            is_first_pitch = True

            if is_new_founder:
                print 'is external founder'
                #first submission from a founder we haven't contacted before, so email them
                to_email = founder.email
                subject = "Your application to %s" % competition.name
                application_url = request.build_absolute_uri("/apply/pitch/%s/?f=%s" % (competition_url, founder.anon_key()))
                message = """Thanks for applying to %s!

The link below will allow you to edit your application any time until judging begins:

%s""" % (competition.name, application_url)
                                               
                send_email(subject, message, to_email)


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


    

    if is_first_pitch:
        #show 1st time sweet success message
        copy = get_custom_copy('thanks for applying', competition)
        return render_to_response('entercompetition/submitted_pitch.html', locals())

    else:
        alert = "Your changes have been saved."
        return HttpResponseRedirect('/apply/pitch/%s/' % competition.hosted_url)



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

    return render_to_response(competition.template_pitch, locals())



def handle_uploaded_file(request, f, upload, pitch):

    upload_path = '%suploads/' % MEDIA_ROOT
    if not os.path.isdir(upload_path):
        os.mkdir(upload_path)
        
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
                except: print 'failed to set attr: %s' % key

        try: callback_function = request.GET["callback_function"]
        except: pass

        try:
            duplicate_founder = Founder.objects.get(email=founder.email)
        except:
            duplicate_founder = None

        if duplicate_founder:
            message = """Sorry, that email has already been used to create an account.\
\
You can either <a href='/apply/pitch/%s/'>visit the competition pitch page</a> or <a href='/apply/load/%s/'>recover your login link from your email</a>""" % (competition.hosted_url, competition.hosted_url)

        else: 

        
            founder.save()

            print 'trying to add founder to competition'
            competition.applicants.add(founder)
            print 'added'

            application_url = "/apply/pitch/%s/?f=%s" % (competition_url, founder.anon_key())

            message = """<p>\
You're registered for the\ competition and will receive email updates as the deadline approaches.\
</p>\
<p style='font-size:18px;'>\
<a href='%s'>Go fill out the application form right now</a>\
</p>\
""" % application_url

            subject = "Application to %s" % competition.name
            to_email = founder.email
            
            email_message = """Thanks for applying to %s!

The link below will allow you to edit your application any time until judging begins:

%s""" % (competition.name, application_url)
                                               
            send_email(subject, email_message, to_email)
           
    else:
        message = "Sorry, the application service is temporarily down. Please try again soon."

    print '1'
    params = '{ "message": "%s"}' % message
    print '2'
    response = "%s( %s )" % (callback_function, params)
    print '3'
    print 'RESPONSE: %s' % response

    return HttpResponse(response, mimetype="application/javascript")


