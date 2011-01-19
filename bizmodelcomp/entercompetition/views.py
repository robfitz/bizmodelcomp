from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect

#saving file uploads
from utils.util import rand_key
import os
import sys

from settings import MEDIA_ROOT

from competition.models import *
from sitecopy.models import SiteCopy
from sitecopy.util import get_custom_copy
from emailhelper.util import send_email

#file uploads to scribd
from settings import SCRIBD_UPLOAD_URL
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
from xml.dom import minidom



#user has claimed to have already submitted an application, so we're
#going to give them some extra info about how to get back to their old
#version and send them a reminder email if needed
def recover_application(request, competition_url):

    competition = Competition.objects.get(hosted_url=competition_url)

    intro = SiteCopy.objects.get(id='recover_application_intro')
    security = SiteCopy.objects.get(id='recover_application_security')

    application_url = "/apply/pitch/%s/" % competition.hosted_url
    cancel = "<a href='%s'>Cancel and apply with a different email</a>" % application_url

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

            application_url = request.build_absolute_uri("/apply/pitch/%s/?f=%s" % (competition.hosted_url, matching_founder.anon_key()))
    
            message = """Hello,

You're receiving this because you requested a reminder link for your application to %s!

You can use go here to edit your application any time until judging begins:
%s

Please feel free to respond to this email if you're still not able to access your application or if you have any other questions or confusion with using the site.

Sincerely,

The %s team""" % (competition.name, application_url, competition.name)
            
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

    copy = """We've sent an email with a login link to the address you just submitted. After clicking that link, you'll be asked to type in your email one last time.

Jumping through these hoops helps ensure your pitch stays private -- sorry for the hassle!"""

    return render_to_response('entercompetition/sent_reminder.html', locals())


#helper
def get_founder(request):

    founder = None

    #figure out which user this is for

    if 'f' in request.GET:

        #TODO: log out current user

        #using an anon link
        rand_key = request.GET.get("f")
        key = AnonFounderKey.objects.get(key=rand_key)
        founder = key.founder
        
        request.session ['founder_key'] = key.key

    elif request.session.get('founder_key', False):

        #TODO: log out current user

        #not logged in, but key is in session
        rand_key = request.session.get('founder_key')
        key = AnonFounderKey.objects.get(key=rand_key)
        founder = key.founder

    return founder



#helper
def send_welcome_email(request, founder, competition):

    to_email = founder.email
    subject = "Your application to %s" % competition.name
    application_url = request.build_absolute_uri("/a/%s/?t=%s" % (competition.hosted_url, founder.anon_key()))
    message = """Hello,

Thanks for applying to %s!

You can use go here to edit your application any time until judging begins:
%s

Please feel free to respond to this email with any questions or confusion with the application process.

Sincerely,

The %s team""" % (competition.name, application_url, competition.name)
                                               
    send_email(subject, message, to_email)




def submit_pitch_get_founder(request, alerts):

    #do we recognize that email?
    mystery_founder = None
    try:
        mystery_founder = Founder.objects.get(email=email)
        if mystery_founder.require_authentication:
            #TODO: need to authenticate via email URL.
            return HttpResponseRedirect('/apply/load/%s/?e=%s' % (competition_url, email))
        else:
            #no auth needed, so just save it as a pitch

            #log in to session
            request.session['founder_key'] = mystery_founder.anon_key()
            
            #now that there's a pitch, we want them to identify
            #themselves from now on
            mystery_founder.require_authentication = True
            mystery_founder.save()
            
            founder = mystery_founder
            is_new_founder = True
        
    except:
        #we don't have a founder on record who matches that email

        #TODO: create a skeleton Founder object & redirect them to
        #application form to fill in the rest of the details

        #create founder
        founder = Founder(email=email)
        founder.save()
        is_new_founder = True

        competition.applicants.add(founder)
        competition.save()

        print '*** saved founder & comp'

        #log in
        request.session['founder_key'] = founder.anon_key()

        print '*** updated session'


def save_pitch_answers_uploads(request, pitch):
        #deal w/ saved answers
        for key in request.POST:

            if key.startswith("question_"):
                question_pk = key[len("question_"):]
                question = PitchQuestion.objects.get(pk=question_pk)

                answer = None
                try:
                    #existing answer?
                    answer = PitchAnswer.objects.get(pitch=pitch, question=question)
                    answer.answer = request.POST[key]
                except:                    
                    #new answer
                    answer = PitchAnswer(question=question,
                                         pitch=pitch,
                                         answer=request.POST[key])
                #save changes
                answer.save()

        #deal w/uploads
        for file in request.FILES:
            upload_pk = file[len("upload_"):]
            upload = PitchUpload.objects.get(pk=upload_pk)
            handle_uploaded_file(request, request.FILES[file], upload, pitch)

def submit_team(request, comp_url):
    
    print 'submit team' 

    alert = None

    founder = get_founder(request)

    competition = get_object_or_404(Competition, hosted_url=comp_url)

    name = ""
    email = ""
    phone = ""
    team_name = ""

    founder = None

    if request.method == "POST":

        email = request.POST.get("email")

        if not email or len(email) == 0:
            #blank email address, display error
            alert = "Please enter a valid email address to continue."

        elif Founder.objects.filter(email=email).count() > 0:
            #email address has already been claimed
            existing_founder = Founder.objects.get(email=email)

            #if this session has validated the email, then proceed
            try:
                founder_key = request.session["founder_key"]
                anon_key = AnonFounderKey(key=founder_key)
                if anon_key.founder == existing_founder:
                    #our session is linked to the founder who owns this
                    #team, so we're good to proceed
                    founder = existing_founder
                else:
                    #if isn't validated this session, offer login link
                    alert = "You have already begun applying with that email. <a href=''>Click here to recover your old application</a>."

            except:
                alert = "You have already begun applying with that email. <a href=''>Click here to recover your old application</a>."

        else: 
            #not blank and not owned by someone else, proceed
            founder = Founder(email=email)
            founder.save()
            request.session["founder_key"] = founder.anon_key().key

        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        team_name = request.POST.get("team_name", "")

        #set other, less critical founder details
        if founder is not None:
            founder.name = request.GET.get("name", "")
            founder.phone = request.GET.get("phone", "")
            founder.save()

        else:
            #founder is none, so we'll just abort out and display the fields again
            return render_to_response("entercompetition/team.html", locals())

        try:
            #look for a team matching this phase and owner
            pitch = Pitch.objects.get(phase=competition.current_phase,
                    team__owner=founder)
            team = pitch.team
        except:
            pitch = None
            team = None

        if not team:
            #create a team if we don't yet have one
            team = Team(owner=founder,
                    name=team_name)
            team.save()

        if not pitch:
            #create a dummy pitch to match the team
            pitch = Pitch(team=team,
                    owner=founder,
                    phase=competition.current_phase)
            pitch.save()

        #set team info
        team.name = team_name
        team.save()

        return HttpResponseRedirect("/a/%s/pitch/" % competition.hosted_url)

    return render_to_response("entercompetition/team.html", locals())



def submit_business(request, comp_url):

    print 'submit business'

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    founder = get_founder(request)

    alert = None
    pitch = None
    team = None

    if not founder:
        return HttpResponseRedirect("/a/%s/" % comp_url)

    try:
        pitch = Pitch.objects.get(phase=competition.current_phase,
                team__owner=founder)
        team = pitch.team
    except:
        pass

    if not team:
        team = Team(owner=founder)
        team.save

    if not pitch:
        pitch = Pitch(team=team,
                owner=founder,
                phase=competition.current_phase)
        pitch.save()

    if request.method == "POST":
        #creates or modifies answers and uploads for the pitch
        save_pitch_answers_uploads(request, pitch)
        print 'saved answers and uploads'

        #if we've already got a founder, we don't let them change the email field
        if not founder:
            email = request.POST.get("email")
            print 'no founder, email=%s' % email

            if email and len(email.split("@")) == 2 and len(email.split(".")) >= 2:
                is_validated = True
                print 'email validated'
            else:
                is_validated = False
                alert = "Your application has __not__ yet been saved. Please enter your team information with a valid email address and try again."
                print 'email failed validation'

        name = request.POST.get("name")

        if competition.application_requirements().institutions.count() > 0:
            institution = request.POST.get("institution")
        if competition.application_requirements().applicant_types.count() > 0:
            applicant_types = request.POST.get("applicant_types")

        team_name = request.POST.get("team_name")

        if competition.application_requirements().locations.count() > 0:
            locations = request.POST.get("locations")

        if not alert:
            alert = "Your application has been saved. You may continue to edit it until the deadline. If you switch computers, you'll need to re-verify your identity by clicking on the link we've emailed to you."
            print 'application saved successfully'
            
    phase = competition.current_phase
    questions = phase.questions()
    uploads = phase.uploads()
    
    for question in questions:
        #render existing answers
        try:
            question.answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)
            
        except:
            question.answer = ""
            
    for upload in uploads:
        #render existing uploads
        try: upload.file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
        except: upload.file = None

    return render_to_response('entercompetition/business.html', locals())



def submit_pitch(request, competition_url):

    competition = Competition.objects.get(hosted_url=competition_url)
    phase = competition.current_phase 
    founder = get_founder(request)
    team = None

    pitch = None
    is_first_pitch = False

    alerts = {}

    #if true, user registered via data import rather than through widget,
    #so we haven't yet sent them a recovery email
    is_new_founder = False 

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
    else:
        #we do have a founder, so may also have a team they belong to and a pitch
        #they've submitted
        try: 
            pitch = Pitch.objects.get(team__owner=founder, phase=phase)
            team = pitch.team
        except: 
            pass


    if phase.is_judging_enabled and not request.GET.get('ignorejudging'):
        #sorry, applications are closed :(((
        message = """Sorry, applications for this phase of the competition are closed and judging has begun."""
        
        return render_to_response('util/message.html', locals())

    if request.method == "POST" and len(request.POST) > 0:

        validated = True

        #this field should be present in the form whenever founder==None
        email = request.POST.get("email")
        if not founder:
            if not email:
                alerts["email"] = "Please enter a valid email address."
                validated = False
            elif len(email.split("@")) < 2 or len(email.split(".")) < 2:
                #extremely basic syntax checking for valid emails
                alerts["email"] = "Please enter a valid email address."
                validated = False

        if competition.application_requirements().institutions.count() > 0:
            institution = request.POST.get("institution")
        if competition.application_requirements().applicant_types.count() > 0:
            applicant_types = request.POST.get("applicant_types")

        team_name = request.POST.get("team_name")
        if not team_name:
            alerts["team_name"] = "You need to enter a team name."

        if competition.application_requirements().locations.count() > 0:
            locations = request.POST.get("locations")



        if not pitch:
            #don't create pitch until someone submits the form
            print 'pitch = NOne, creating new'
            pitch = Pitch(owner=founder,
                          phase=phase)
            if validated:
                pitch.save()

            #can show different success message on first submission
            is_first_pitch = True

            if is_new_founder:
                print 'is external founder'
                #first submission from a founder we haven't contacted before, so email them
                send_welcome_email(request, founder, competition)

        save_pitch_answers_uploads(request, pitch)

        if not validated:
            #hasn't validated, so re-load page with same answers etc
            return render_to_response("/a/%s/" % competition.hosted_url, locals())


        else:

            if not founder:
                founder = Founder()
                founder.save()

            founder.name = founder_name
            founder.email = founder_email
            founder.phone = founder_phone
            founder.save()

            pitch.founder = founder
            pitch.save()

            if not team:
                team = Team()
                team.save()

            team.owner = founder
            team.name = team_name
            team.save()

    if is_first_pitch:
        #show 1st time sweet success message
        copy = get_custom_copy('thanks for applying', competition)
        return render_to_response('entercompetition/submitted_pitch.html', locals())

    else:
        copy = get_custom_copy('thanks for applying', competition)
        return render_to_response('entercompetition/submitted_pitch.html', locals())

        #alert = "Your changes have been saved."
        #return HttpResponseRedirect('/apply/pitch/%s/' % competition.hosted_url)



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
    else: phase = competition.current_phase 

    if phase.is_judging_enabled and not request.GET.get('ignorejudging', False):
        #sorry, applications are closed :(((
        message = """Sorry, applications for this phase of the competition are closed and judging has begun."""

        return render_to_response('util/message.html', locals())


    try: 
        pitch = Pitch.objects.filter(owner=founder).get(phase=phase)
    except: 
        pitch = None
        
    questions = phase.questions()
    uploads = phase.uploads()
    
    for question in questions:
        #render existing answers
        try:
            question.answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)
            
        except:
            question.answer = ""
            
    for upload in uploads:
        #render existing uploads
        try: upload.file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
        except: upload.file = None

    #return render_to_response(competition.template_pitch, locals())
    return render_to_response('entercompetition/pitch_form.html', locals())



def handle_uploaded_file(request, f, upload, pitch):

    upload_path = '%suploads/' % MEDIA_ROOT
    if not os.path.isdir(upload_path):
        os.mkdir(upload_path)
        
    file_name = ""
    
    #add to a random directory to avoid collisions
    rand_folder = rand_key(20)
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

    #send file to scribd for display
    register_openers()

    datagen, headers = multipart_encode({"file": open(pitch_file.file_location, "rb")})
    request = urllib2.Request(SCRIBD_UPLOAD_URL, datagen, headers)

    #xml with <doc_id>, <access_key>, and <secret_password>
    scribd_response = urllib2.urlopen(request).read()
    print 'Scribd response: %s' % scribd_response
    xml = minidom.parseString(scribd_response)
    try:
        doc_id = xml.getElementsByTagName("doc_id")[0].firstChild.data
        access_key = xml.getElementsByTagName("access_key")[0].firstChild.data
        secret_password = xml.getElementsByTagName("secret_password")[0].firstChild.data

        scribd_file_data = None
        try:
            scribd_file_data = ScribdFileData.objects.get(pitch_file=pitch_file)
            scribd_file_data.doc_id = doc_id
            scribd_file_data.access_key = access_key
            scribd_file_data.secret_password = secret_password
        except:
            scribd_file_data = ScribdFileData(pitch_file=pitch_file,
                    doc_id=doc_id,
                    access_key=access_key,
                    secret_password=secret_password)

        scribd_file_data.save()
        
    except:
        #no scribd file basically means it was a non-doc (image etc)
        print 'Scribd exception: %s' % sys.exc_info()[0]
        try:
            #we might have an old upload that _did_ use scribd for this upload, 
            #in which case we scrap it
            scribd_file_data = ScribdFileData.objects.get(pitch_file=pitch_file)
            scribd_file_data.delete()
        except:
            pass

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
                try: 
                    setattr(founder, key, request.GET[key])
                except: 
                    print 'failed to set attr: %s' % key

        try: 
            callback_function = request.GET["callback_function"]
        except: 
            pass

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

            send_welcome_email(request, founder, competition)
           
    else:
        message = "Sorry, the application service is temporarily down. Please try again soon."

    print '1'
    params = '{ "message": "%s"}' % message
    print '2'
    response = "%s( %s )" % (callback_function, params)
    print '3'
    print 'RESPONSE: %s' % response

    return HttpResponse(response, mimetype="application/javascript")


