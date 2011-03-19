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



def terms_of_service(request, comp_url):

    competition = get_object_or_404(Competition, hosted_url=comp_url)

    copy = competition.terms_of_service

    return render_to_response('sitecopy/static_copy_popup_nowidget.html', locals())
    #return render_to_response('entercompetition/terms_of_service.html', locals())



#user has claimed to have already submitted an application, so we're
#going to give them some extra info about how to get back to their old
#version and send them a reminder email if needed
def recover_application(request, competition_url):

    competition = Competition.objects.get(hosted_url=competition_url)

    intro = SiteCopy.objects.get(id='recover_application_intro')
    security = SiteCopy.objects.get(id='recover_application_security')

    application_url = "/a/%s/" % competition.hosted_url
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

            application_url = request.build_absolute_uri("/a/%s/?f=%s" % (competition.hosted_url, matching_founder.anon_key()))
    
            message = """Hello,

You're receiving this because you requested a reminder link for your application to %s!

You can use go here to edit your application any time until judging begins:
%s

Please feel free to respond to this email if you're still not able to access your application or if you have any other questions or confusion with using the site.

Sincerely,

The %s team""" % (competition.name, application_url, competition.name)
            
            
            send_email(subject, message, email)

            return HttpResponseRedirect('/apply/sent_reminder/')
            
        except:
            #couldn't find a matching founder. tell person to apply now or re-type
            application_url = "/a/%s/" % competition.hosted_url
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
    application_url = request.build_absolute_uri("/a/%s/?f=%s" % (competition.hosted_url, founder.anon_key()))
    message = """Hello,

Thanks for applying to %s!

You can use go here to edit your application any time until judging begins:
%s

Please feel free to respond to this email with any questions or confusion with the application process.

Sincerely,

The %s team""" % (competition.name, application_url, competition.name)
                                               
    send_email(subject, message, to_email)



def save_pitch_answers_uploads(request, pitch):
        #deal w/ saved answers
        for key in request.POST:

            if key.startswith("question_"):
                question_pk = key[len("question_"):]
                question = PitchQuestion.objects.get(pk=question_pk)

                answer = None
                answer_text = unicode(request.POST.get(key, "").encode('unicode_escape'))

                try:
                    #existing answer?
                    possible_answers = PitchAnswer.objects.filter(pitch=pitch).filter(question=question)

                    answer = possible_answers[0]
                    answer.answer = answer_text
                    #answer.answer = unicode(request.POST.get(key, "").encode('unicode_escape'))
                except:                    
                    #new answer
                    answer = PitchAnswer(question=question,
                                         pitch=pitch,
                                         answer=answer_text)
                #save changes
                answer.save()


        #deal w/uploads
        for file in request.FILES:
            upload_pk = file[len("upload_"):]
            upload = PitchUpload.objects.get(pk=upload_pk)
            handle_uploaded_file(request, request.FILES[file], upload, pitch)

def submit_team(request, comp_url):
    
    alert = None

    founder = get_founder(request)

    competition = get_object_or_404(Competition, hosted_url=comp_url)

    if 'f' in request.GET:

        #TODO: log out current user

        #using an anon link
        try:
            rand_key = request.GET.get("f")
            key = AnonFounderKey.objects.get(key=rand_key)
            founder = key.founder
        
            request.session['founder_key'] = key.key
            return HttpResponseRedirect("/a/%s/pitch/" % comp_url)
        except:
            pass

    if founder is not None:
        pitches_1 = Pitch.objects.filter(phase=competition.current_phase,
                owner=founder)
        pitches_2 = Pitch.objects.filter(phase=competition.current_phase,
                team__owner=founder)

        if len(pitches_1) > 0 or len(pitches_2) > 0:
            return HttpResponseRedirect("/a/%s/pitch/" % comp_url)


    #standard team info
    name = ""
    email = ""
    team_name = ""

    #less common, optional team info
    phone = ""
    address = ""
    birthday = ""
    course_of_study = ""
    year_of_study = ""

    founder = None

    if request.method == "POST":

        email = request.POST.get("email")
        team_name = request.POST.get("team_name", "")

        if not email or len(email) == 0:
            #blank email address, display error
            alert = "Please enter a valid email address to continue."

        elif not team_name or len(team_name) == 0:
            alert = "Please enter your team name to continue."

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
                    alert = "You have already begun applying with that email. <a href='/apply/load/%s/'>Click here to recover your old application</a>." % competition.hosted_url

            except:
                alert = "You have already begun applying with that email. <a href='/apply/load/%s/'>Click here to recover your old application</a>." % competition.hosted_url

        else: 
            #not blank and not owned by someone else, proceed
            founder = Founder(email=email)
            founder.save()
            request.session["founder_key"] = founder.anon_key().key

        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")

        applicant_type = request.POST.get("applicant_types", "")
        location = request.POST.get("locations", "")
        institution = request.POST.get("institution", "")

        birthday = request.POST.get("birthday", "")
        address = request.POST.get("address", "")
        course_of_study = request.POST.get("course_of_study", "")
        year_of_study = request.POST.get("year_of_study", "")

        #set other, less critical founder details
        if founder is not None:

            founder.name = name.encode('unicode_escape')
            founder.phone = phone.encode('unicode_escape')

            founder.birth = birthday.encode('unicode_escape')
            founder.address = address.encode('unicode_escape')
            founder.course_of_study = course_of_study.encode('unicode_escape')
            founder.year_of_study = year_of_study.encode('unicode_escape')

            if applicant_type:
                try:
                    tag = Tag.objects.get(name=applicant_type.encode('unicode_escape'))
                except:
                    tag = Tag(name=applicant_type.encode('unicode_escape'))
                    tag.save()
                founder.applicant_type = tag

            if location:
                try:
                    tag = Tag.objects.get(name=location.encode('unicode_escape'))
                except:
                    tag = Tag(name=location.encode('unicode_escape'))
                    tag.save()
                founder.location = tag

            if institution:
                try:
                    tag = Tag.objects.get(name=institution.encode('unicode_escape'))
                except:
                    tag = Tag(name=institution.encode('unicode_escape'))
                    tag.save()
                founder.institution = tag

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
                    name=unicode(team_name).encode('unicode_escape'))
            team.save()

        if not pitch:
            #create a dummy pitch to match the team
            pitch = Pitch(team=team,
                    owner=founder,
                    phase=competition.current_phase)
            pitch.save()

            #if a pitch has just been created, that suggests this is the first time
            #the founder has applied to this particular competition, so we're gonna
            #email them
            send_welcome_email(request, founder, competition)

        #set team info
        team.name = unicode(team_name).encode('unicode_escape')
        team.save()

        #reset additional teammates
        for teammate in team.other_members.all():
            team.other_members.remove(teammate)

        #init additional teammates
        for key in request.POST:
            if key.startswith("teammate-email_"):
                num = key[len("teammate-email_"):]
                teammate_email = request.POST.get(key)
                teammate_name = unicode(request.POST.get("teammate-name_%s" % num, teammate_email.split('@')[0])).encode('unicode_escape')
                teammate = None
                try:
                    teammate = Founder.objects.get(email=teammate_email)
                except:
                    teammate = Founder(email=teammate_email,
                            name=teammate_name)
                    teammate.save()
                team.other_members.add(teammate)
        team.save()

        print 'saving team, looking to add founder to applicants'
        if founder not in competition.applicants.all():
            competition.applicants.add(founder)
            print 'added founder(%s) to competition applicants, len=%s' % (founder, competition.applicants.count())
        else:
            print 'didnt add founder to comp applicants'

        for teammate in team.other_members.all():
            if teammate not in competition.applicants.all():
                competition.applicants.add(teammate)

        return HttpResponseRedirect("/a/%s/pitch/" % competition.hosted_url)

    return render_to_response("entercompetition/team.html", locals())



def submit_business(request, comp_url):

    print 'submit business'
    log = ""

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    alert = None
    pitch = None
    team = None
    business_types = None

    founder = get_founder(request)
    
    if not founder:
        return HttpResponseRedirect("/a/%s/" % comp_url)

    try:
        log += "trying!"
        pitch = Pitch.objects.get(phase=competition.current_phase,
                team__owner=founder)
        team = pitch.team
        log += "1"
    except:
        try:
             
            pitches = Pitch.objects.filter(phase=competition.current_phase,
                    team__owner=founder)
            pitch = pitches[len(pitches)-1]
            log += "2"
        except:
            try:
                pitch = Pitch.objects.get(phase=competition.current_phase,
                        owner=founder)
                team=None
                log += "3" 
            except:
                pitches = Pitch.objects.filter(phase=competition.current_phase,
                        owner=founder)
                team=None
                if pitches is not None and len(pitches) > 0:
                    pitch = pitches[len(pitches)-1]
                log += "4"



    if not team:

        log += "no team"
        team = Team(owner=founder)
        team.save
        log += ", made team=(%s)" % team

    if not pitch:
        log += ", no pitch"
        pitch = Pitch(team=team,
                owner=founder,
                phase=competition.current_phase)
        pitch.save()
        log += ", made pitch=(%s)" % pitch

    team.save()
    pitch.team = team
    pitch.save()

    if request.method == "POST":
        #creates or modifies answers and uploads for the pitch
        save_pitch_answers_uploads(request, pitch)

        if competition.application_requirements().applicant_types.count() > 0:
            business_type = request.POST.get("business_types")
            for t in team.business_types.all():
                team.business_types.remove(t)
            if business_type is not None:
                tag = None
                try:
                    tag = Tag.objects.get(name=business_type)
                except:
                    tag = Tag(name=business_type)
                    tag.save()
                team.business_types.add(tag)

        if not alert:
            alert = "Congratulations! Your application has been saved and submitted. You may continue to edit your application until the deadline. If you have finished editing your application you need take no further action."
            
    phase = competition.current_phase
    questions = phase.questions()
    uploads = phase.uploads()
    
    for question in questions:
        #render existing answers
        try:
            print 'try getting answer for pitch %s' % pitch.id
            answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)
            print 'got answer %s' % answer.id
            question.answer = unicode(answer)
            print 'set answer unicode'

            print 'set question (%s) answer: %s' %  (question.id, question.answer)

            #unicode(PitchAnswer.objects.filter(pitch=pitch).get(question=question)).decode('unicode-escape')
            
        except:
            possible_answers = PitchAnswer.objects.filter(pitch=pitch).filter(question=question)
            if len(possible_answers) > 0:
                answer = possible_answers[0]
                question.answer = unicode(answer) 
            else:
                question.answer = ""
            
    for upload in uploads:
        #render existing uploads
        try: upload.file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
        except: upload.file = None

    return render_to_response('entercompetition/business.html', locals())



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


