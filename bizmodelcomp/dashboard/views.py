from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from competition.models import *
from judge.models import *
from dashboard.forms import *
from dashboard.util import *
import time
import smtplib


#edit phases
@login_required
def edit_phases(request, competition_id):

    if not has_dash_perms(request, competition_id):
       return HttpResponseRedirect("/no_permissions/")

    if request.method == "POST":

        try: phase = Phase.objects.get(id=request.POST.get("phase_id", None))
        except:
            if "new_phase" in request.POST:
                phase = Phase(competition=Competition.objects.get(id=competition_id))

        if phase:
            print 'got phase %s' % phase
            print request.POST.get("is_deleted", "absent")
            form = PhaseForm(request.POST, instance=phase)
            form.save()

            phase.is_deleted = request.POST.get("is_deleted") == "on"
            phase.save()

        return HttpResponseRedirect("/dashboard/%s/phases/" % competition_id)

    phases = Phase.objects.filter(competition__id=competition_id).filter(is_deleted=False)
    for phase in phases:

        phase.form = PhaseForm(instance=phase)

    new_phase = Phase()
    new_form = PhaseForm(instance=new_phase)

    return render_to_response("dashboard/edit_phases.html", locals())



#organizer has chosen to remove the jduging permissions from
#some number of judges for this phase via the dashboard.
@login_required
def delete_judge_invites(request, competition_id, phase_id):

    if not has_dash_perms(request, competition_id):
        return HttpResponseRedirect("/no_permissions/")

    if request.method == "POST" and len(request.POST) > 0:

        if "action" in request.POST:
            action = request.POST["action"]
            if action == "delete_selected":

                for key in request.POST:

                    if key.startswith("is_selected_") and request.POST[key] == "on":

                        id = int(key[len("is_selected_"):])

                        invites = JudgeInvitation.objects.filter(competition__id=competition_id).filter(id=id)

                        for i in invites:
                            print 'delete invite %s with email %s' % (i, i.email)
                            i.delete()

    return HttpResponseRedirect('/dashboard/%s/phase/%s/judges/' % (competition_id, phase_id))

    

#organizer is looking at a list of all the current judges and their performance thus far,
#with options to modify their role
@login_required
def list_judges(request, competition_id, phase_id):

    if not has_dash_perms(request, competition_id):
        return HttpResponseRedirect("/no_permissions/")

    #new judges are invited from a small form on the single management/list page,
    #so if it's a post we're going to be inviting a new judge
    if request.method == "POST" and len(request.POST) > 0:

        email = request.POST["invite_list"]

        if len(JudgeInvitation.objects.filter(competition__id=competition_id).filter(email=email)) != 0:
            #if we already have a judge for this competition with that email, alert
            #the organizer that nothing needs to happen
            error = "You've already invited that judge."
        else:
            #otherwise, if we haven't already invited this judge, add them
            #to the system and invite them
            invite = JudgeInvitation(competition__id=competition_id,
                                     email=email)
            invite.save()
            
            #tell them they're a winner
            judging_link = request.build_absolute_uri("/judge/")
            invite.send_invitation_email(judging_link)

    judge_invitations = JudgeInvitation.objects.filter(competition__id=competition_id)
    return render_to_response("dashboard/list_judges.html", locals())
    
    

#view at the scores a judge has previously assigned to a pitch pitch pitch.
#if the person viewing is the same person who made the original judgement,
#they should also be able to edit their answers.
@login_required
def view_judgement(request, judgement_id):

    try:
        judged_pitch = JudgedPitch.objects.get(id=judgement_id)
        pitch = judged_pitch.pitch
        can_edit = False

        if judged_pitch.judge.user == request.user:
            #original judge can view & revise
            can_edit = True
        elif pitch.phase.competition.owner == request.user:
            #organizer can view but not edit
            pass
        else:
            #different judges and other randoms can't see it
            return HttpResponseRedirect("/no_permissions/")
    except:
        #unrecognized pitch or judgement
        return HttpResponseRedirect("/no_permissions/")

    questions = pitch.phase.questions()
    uploads = pitch.phase.uploads()

    for question in questions:
        try:
            question.answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)
            try:
                question.judged_answer = JudgedAnswer.objects.filter(judged_pitch=judged_pitch).get(answer=question.answer)
            except:
                question.judged_answer = None
        except:
            question.answer = None
        
    for upload in uploads:
        try: upload.file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
        except: upload.file = None

    return render_to_response("dashboard/view_judgement.html", locals())
            
    

@login_required
def view_pitch(request, pitch_id):

    try:
        pitch = Pitch.objects.get(id=pitch_id)
        if pitch.phase.competition.owner != request.user:
            return HttpResponseRedirect("/no_permissions/")
    except:
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

    #permissions?
    try:
        competition = Competition.objects.get(pk=competition_id)
        
        if not competition.owner == request.user:
            return HttpResponseRedirect("/no_permissions/")        
    except:
        return HttpResponseRedirect("/no_permissions/")

    
    return render_to_response("dashboard/list_applicants.html", locals())


@login_required
def list_judgements(request, competition_id, phase_id, judge_id):

    judge = JudgeInvitation.objects.get(id=judge_id)
    competition = Competition.objects.get(id=competition_id)
    phase = Phase.objects.filter(competition=competition).get(id=phase_id)

    #has permissions?
    has_perms = False

    #is an organizer?
    if request.user == competition.owner:
        has_perms = True

    #is the judge in question?
    elif request.user == judge.user:
        has_perms = True

    if not has_perms:
        return HttpResponseRedirect("/no_permissions/")

    judged_pitches = JudgedPitch.objects.filter(pitch__phase__id=phase_id).filter(judge__id=judge_id)

    return render_to_response("dashboard/list_judged_pitches.html", locals())
    


#view list of pitches, sort & manipulate them
@login_required
def list_pitches(request, competition_id, phase_id, judge_id=None):

    #are comp & phase valid?
    try:
        competition = Competition.objects.get(id=competition_id)
        phase = Phase.objects.filter(competition=competition).get(id=phase_id)
    except:
        return HttpResponseRedirect("/no_permissions/")


    #is organizer?
    if competition.owner == request.user:
        return render_to_response("dashboard/list_pitches.html", locals())

    else:
        return HttpResponseRedirect("/no_permissions/")
    


#view & manage your competitions
@login_required
def dashboard(request):

    #find if user is the organizer for.. something
    competitions = Competition.objects.filter(owner = request.user)

    if len(competitions) == 0:
        
        return HttpResponseRedirect("/no_permissions/")

    else:
    
        competition = competitions[0]

        organizer_judge = None

        try:
            organizer_judge = JudgeInvitation.objects.filter(competition=competition).get(user=competition.owner)
        except:
            pass
        
        return render_to_response("dashboard/dashboard.html", locals())



#view list of applicants, sort & manipulate them
@login_required
def manage_applicants(request, competition_id):

    competition = Competition.objects.get(pk=competition_id)
    print competition.applicants.all()

    return render_to_response("competition/manage_applicants.html", locals())

