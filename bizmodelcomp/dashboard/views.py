from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from competition.models import *
from judge.models import *
import time
import smtplib

@login_required
def delete_judge_invites(request, competition_id, phase_id):

    #are comp & phase valid?
    try:
        competition = Competition.objects.get(id=competition_id)
        phase = Phase.objects.filter(competition=competition).get(id=phase_id)
    except:
        return HttpResponseRedirect("/no_permissions/")

    #is organizer?
    if not competition.owner == request.user:
        return HttpResponseRedirect("/no_permissions/")

    if request.method == "POST" and len(request.POST) > 0:

        if "action" in request.POST:
            action = request.POST["action"]
            if action == "delete_selected":

                for key in request.POST:

                    if key.startswith("is_selected_") and request.POST[key] == "on":

                        id = int(key[len("is_selected_"):])

                        invites = JudgeInvitation.objects.filter(competition=competition).filter(id=id)

                        for i in invites:
                            print 'delete invite %s with email %s' % (i, i.email)
                            i.delete()

    return HttpResponseRedirect('/dashboard/%s/phase/%s/judges/' % (competition_id, phase_id))
    

@login_required
def list_judges(request, competition_id, phase_id):

    #are comp & phase valid?
    try:
        competition = Competition.objects.get(id=competition_id)
        phase = Phase.objects.filter(competition=competition).get(id=phase_id)
    except:
        return HttpResponseRedirect("/no_permissions/")

    #is organizer?
    if not competition.owner == request.user:
        return HttpResponseRedirect("/no_permissions/")

    if request.method == "POST" and len(request.POST) > 0:

        email = request.POST["invite_list"]
        
        #TODO: cache query instead of this disaster...
        current_invites = JudgeInvitation.objects.filter(competition=competition)
        current_emails = []
        
        for invite in current_invites:
            current_emails.append(invite.email)

        smtp = smtplib.SMTP('smtp.sendgrid.net')        

        if email not in current_emails:
            
            #new invite!
            invite = JudgeInvitation(competition=competition,
                                     email=email)
            invite.save()
            
            #tell them they're a winner
            invite.send_invitation_email()
        
    judge_invitations = JudgeInvitation.objects.filter(competition=competition)

    return render_to_response("dashboard/list_judges.html", locals())
    


@login_required
def invite_judges(request, competition_id, phase_id):

    #are comp & phase valid?
    try:
        competition = Competition.objects.get(id=competition_id)
        phase = Phase.objects.filter(competition=competition).get(id=phase_id)
    except:
        return HttpResponseRedirect("/no_permissions/")


    #is organizer?
    if not competition.owner == request.user:
        return HttpResponseRedirect("/no_permissions/")


    if request.method == "POST" and len(request.POST) > 0:

        raw = request.POST["invite_list"]
        lines = raw.splitlines()

        emails_1 = []
        emails_2 = []
        emails_3 = []

        print 'raw: %s' % raw
        print 'lines: %s' % lines

        #split on newline, comma, and semicolon
        for line in lines:
            emails_1.extend(line.split(';'))
        for email in emails_1:
            print 'email 1: %s' % email
            emails_2.extend(email.split(','))
        for email in emails_2:
            print 'email 2: %s' % email
            stripped = email.strip()
            print 'stripped: %s' % stripped
            if stripped and len(stripped) > 0:
                emails_3.append(stripped)

            print 'emails 3: %s' % emails_3
        emails = emails_3

        #TODO: cache query instead of this disaster...
        current_invites = JudgeInvitation.objects.filter(competition=competition)
        current_emails = []
        
        for invite in current_invites:
            current_emails.append(invite.email)

        smtp = smtplib.SMTP('smtp.sendgrid.net')        
        for email in emails:
            #ignore if already invited
            if email not in current_emails:
                #new invite!
                invite = JudgeInvitation(competition=competition,
                                         email=email)
                invite.save()
                
                #tell them they're a winner
                invite.send_invitation_email(smtp)

##                time.sleep(5)

        smtp.quit()
                

        return HttpResponseRedirect("/dashboard/%s/phase/%s/judges/" % (competition_id, phase_id))

    return render_to_response("dashboard/invite_judges.html", locals())

    
            
    

@login_required
def view_pitch(request, pitch_id):

    try:
        print 'getting pitch id=%s' % pitch_id
        pitch = Pitch.objects.get(id=pitch_id)
        print "owner: %s, user: %s" % (pitch.phase.competition.owner, request.user)
        if pitch.phase.competition.owner != request.user:
            return HttpResponseRedirect("/no_permissions/")
    except:
        print "except"
        return HttpResponseRedirect("/no_permissions/")

    questions = pitch.phase.questions()
    uploads = pitch.phase.uploads()

    for question in questions:
        try: question.answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)
        except: question.answer = None
            
    for upload in uploads:
        try: upload.file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
        except: upload.file = None

    return render_to_response("dashboard/view_pitch.html", locals())



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
    competition = competitions[0]

    return render_to_response("competition/dashboard.html", locals())



#view list of applicants, sort & manipulate them
@login_required
def manage_applicants(request, competition_id):

    competition = Competition.objects.get(pk=competition_id)
    print competition.applicants.all()

    return render_to_response("competition/manage_applicants.html", locals())

