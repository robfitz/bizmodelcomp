from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from competition.models import *
from judge.models import *
from dashboard.forms import *
from dashboard.util import *
import charts.util as chart_util
from datetime import datetime
import time
import smtplib



@login_required
def edit_application(request, phase_id):

    phase = Phase.objects.get(id=phase_id)

    if not has_dash_perms(request, phase.competition.id):
        return HttpResponseRedirect("/no_permissions/")

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
                    #create new question
                    if prompt and len(prompt.strip())>0:
                        q = PitchQuestion(phase=phase,
                                        prompt=prompt)
                        q.save()

                elif key.startswith('upload_prompt_'):
                    #create new upload
                    if prompt and len(prompt.strip()) > 0:
                        u = PitchUpload(phase=phase,
                                        prompt=prompt)
                        u.save()
                        
            except: pass
            
        return HttpResponseRedirect("/dashboard/")

    return render_to_response('dashboard/edit_application.html', locals())



MONTH_NUMS = { "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
               "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12 }


#edit phases
@login_required
def edit_phases(request, competition_id):

    if not has_dash_perms(request, competition_id):
       return HttpResponseRedirect("/no_permissions/")


    editing_phase = request.GET.get("open", None)

    if request.method == "POST":

        try: phase = Phase.objects.get(id=request.POST.get("phase_id", None))
        except:
            if "new_phase" in request.POST:
                phase = Phase(competition=Competition.objects.get(id=competition_id))

        if phase:
            form = PhaseForm(request.POST, instance=phase)
            form.save()

            phase.is_deleted = request.POST.get("is_deleted") == "on"
            phase.save()

            date = request.POST.get("date", None)
            hour = int(request.POST.get("hour", 23))
            minute = int(request.POST.get("minute", 59))

            print 'date %s, %s:%s' % (date, hour, minute)
            
            if date is not None:

                year = int(date.split()[3])
                month = MONTH_NUMS[date.split()[2].strip(',')]
                day = int(date.split()[1])
                
                print 'date2 %s, %s, %s' % (year, month, day)

                phase.deadline = datetime(year, month, day, hour, minute)
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
def dashboard(request, phase_id=None):

    #find if user is the organizer for.. something
    competitions = Competition.objects.filter(owner = request.user)

    if phase_id is not None:

        phase = get_object_or_404(Phase, id=phase_id)
        max_score = phase.max_score()
        score_groups = chart_util.score_distribution(phase.judgements(), max(phase.max_score() / 20, 1))
    
    if len(competitions) == 0:
        
        return HttpResponseRedirect("/no_permissions/")

    else:
    
        competition = competitions[0]

        organizer_judge = None

        try:
            organizer_judge = JudgeInvitation.objects.filter(competition=competition).get(user=competition.owner)
        except:
            pass

        phases = Phase.objects.filter(competition=competition).filter(is_deleted=False)
        
        return render_to_response("dashboard/dashboard.html", locals())



#view list of applicants, sort & manipulate them
@login_required
def manage_applicants(request, competition_id):

    competition = Competition.objects.get(pk=competition_id)

    return render_to_response("competition/manage_applicants.html", locals())

