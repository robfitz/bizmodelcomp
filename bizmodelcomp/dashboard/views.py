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
def announce_applications_open(request):

    competition = request.user.get_profile().competition()
    phase = competition.current_phase

    from_email = "competitions@nvana.com"

    subject = "%s - Applications open" % competition.name

    message_template = """Hello,

Applications to __%s__ are now open. You may apply at the following link:

http://www.nvana.com/%s/

You'll be able to submit and revise your application until __%s__. Only one person per team needs to submit an application. 

Thanks for participating. We look forward to your submissions. Please contact the organizer if you have any questions.

Sincerely,

%s team
""" % (competition.name, competition.hosted_url, phase.deadline.strftime("%A, %B %d, %H:%M %p"), competition.name)

    recipients = []
    for founder in phase.applicants():
        if founder.email:
            recipients.append(founder.email)

    confirm_warning = "Are you sure you want to send this email to <strong>%s recipients</strong> and begin accepting pitches? You won't be able to change the application questions after you do this!" % len(recipients)

    messages = []
    for i in range(0, len(recipients) - 1):

        #TODO: use string.parse(format_string) instead of this manual replacing
        message = {}
        message["to_email"] = recipients[i]
        message["body"] = message_template
        #message.body = message_template.replace(message_template, "[[team_name]]", "[[TODO]]")

        messages.append(message)

    return render_to_response('emailhelper/review_email.html', locals())

    

def create_new_comp_for_user(user):
    key = None
    while True: 
        #find a unique url for the competition
        key = rand_key(6)
        try: 	Competition.objects.get(hosted_url=key)
        except:	break
        
    competition = Competition(owner=user, hosted_url=key)
    competition.save()
    current_phase = Phase(competition=competition)
    current_phase.save()
    competition.current_phase = current_phase
    competition.save()

    if not user.get_profile():
        #ensure old accounts have a profile
        profile = UserProfile(user=request.user)
        profile.selected_competition = competition
        profile.save()

    return competition


@login_required
def edit_comp_details(request):

    competition = request.user.get_profile().competition()
    alert = ""

    if not competition:
        return HttpResponseRedirect('/dashboard/setup/1/')


    if request.method == "POST":
        #create model form from POST data
        form = CompetitionInfoForm(request.POST, request.FILES, instance=competition)

        try:
            form.save()
            #success, return to dashboard
            return HttpResponseRedirect("/dashboard/")

        except:
            #form saving failed, alert user and re-display
            alert = "That URL has already been used by someone. Try something else?"
            return render_to_response('dashboard/edit_comp_details.html', locals())

    else: #GET
        form = CompetitionInfoForm(instance=competition)

        return render_to_response('dashboard/edit_comp_details.html', locals())

def setup(request, step_num):
    
    #custom auth handling bc we generally want to redirect to register rather than login
    if not request.user.is_authenticated():
        if step_num == "1":
            return HttpResponseRedirect("/accounts/register/?next=/dashboard/setup/%s/" % step_num)
        else:
            return HttpResponseRedirect("/accounts/login/?next=/dashboard/setup/%s/" % step_num)


    alert = ""

    templates = { "1": "dashboard/setup_comp_details.html",
            "2": "dashboard/setup_app_reqs.html",
            "3": "dashboard/setup_distribution.html" }

    form = None

    if request.method == "POST":

        if step_num == "1":

            #create new competition for user with inputted details
            competition = create_new_comp_for_user(request.user) 

            if not competition:
                #display error if non-unique hosted URL
                alert = "That URL has already been used by someone. Try something different?"

            #create model form from POST data
            form = CompetitionInfoForm(request.POST, instance=competition)

            #save instance
            try:
                form.save()

                #if success, set as user's current competition
                request.user.get_profile().current_competition = competition
                request.user.get_profile().save()

            except:
                                    
                if competition:
                    #delete comp we just created since there was an error saving data
                    #and we don't want half-baked multiples floating around
                    competition.delete()
                    
                alert = "That URL has already been used by someone. Try something different?"


        elif step_num == "2":

            competition = request.user.get_profile().competition

            #save application requirements

        elif step_num == "3":

            #nothing to do, submission is just used to advance to
            #next step
            pass


        #go to next step
        try:
            next_step = ""
            if alert:
                next_step = step_num
                print 'alert: %s' % alert
            else:
                next_step = str(int(step_num) + 1)

            print 'next step: %s' % next_step
            temp = templates[next_step]
            print 'temp: %s' % temp
            #got a submission for the current step, move on to next one
            return HttpResponseRedirect('/dashboard/setup/%s/' % next_step)

        except:
            print 'except: %s' % sys.exc_info()[0]
            #no more steps to show, so go to dashboard
            return HttpResponseRedirect('/dashboard/')

    else: #request.method==GET
        try:
            temp = templates[step_num]

            if step_num == "1":
                form = CompetitionInfoForm()

            elif step_num == "2":
                pass

            print 'get rendering step: %s' % step_num

            #for a GET, just render the relevant template
            return render_to_response(templates[step_num], locals())

        except:
            print 'get except: %s' % sys.exc_info()[0]
            #can't find what they're looking for, back to dash 
            return HttpResponseRedirect('/dashboard/')



def set_question_options(request, question, is_new=False):

    print 'set question options: %s' % question

    id = question.id
    if is_new:
        id = "new%s" % id

    is_required = request.POST.get("is_required_%s" % id, None)
    has_score = request.POST.get("has_score_%s" % id, None)
    max_points = request.POST.get("max_points_%s" % id, 1)
    points_prompt = request.POST.get("points_prompt_%s" % id, "")
    has_feedback = request.POST.get("has_feedback_%s" % id, False)
    feedback_prompt = request.POST.get("feedback_prompt_%s" % id, "")
    show_choices = request.POST.get("show_choices_%s" % id, False)
    choices = request.POST.get("choices_%s" % id, "")

    is_hidden_from_applicants = request.POST.get("is_judge_only_%s" % id, False)

    print 'is hidden from applicants? %s' % is_hidden_from_applicants

    question.is_hidden_from_applicants = is_hidden_from_applicants
    if is_hidden_from_applicants:
        question.prompt = ""
        question.is_required = False
        question.raw_choices = ""

    else:        
        if is_required is not None:
            question.is_required = is_required

        if show_choices:
            question.raw_choices = choices
        else:
            question.raw_choices = ""

    if has_score:
        question.max_points = max_points
        question.judge_points_prompt = points_prompt
    else:
        question.max_points = 0
        question.judge_points_prompt = ""

    if has_feedback:
        question.judge_feedback_prompt = feedback_prompt
    else:
        question.judge_feedback_prompt = ""

    return question


def should_delete(question):

    if question.is_hidden_from_applicants:
        #if the applicant can't see it and there's no instructions
        #for the judges, then delete it
        if not question.max_score and not question.judge_feedback_prompt:

            return True

    else:
        #if there's no instructions for the applicant, delete it
        if not question.prompt:

            return True

    return False


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
                
                if key.startswith('old_question_prompt_'):

                    id  = key[len('old_question_prompt_'):]
                    prompt = request.POST.get(key)
                    
                    if id != 'new' and id.startswith('new'):

                        #create new question
                        if prompt is not None:
                            q = PitchQuestion(prompt=prompt,
                                              phase=phase)
                            q.save()
                            q = set_question_options(request, q, is_new=True)
                            q.save()

                    else:

                        #check if existing question has been edited
                        q = PitchQuestion.objects.get(id=id)
                        
                        if q.prompt != prompt:
                            q.prompt = prompt
                            
                        q = set_question_options(request, q)
                        q.save()

                    if should_delete(q):
                        q.delete()
                                    
                elif key.startswith('old_upload_prompt_'):

                    prompt = request.POST.get(key)
                    
                    id  = key[len('old_upload_prompt_'):]

                    if id != 'new' and id.startswith('new'):
                        #create new upload
                        if prompt and len(prompt.strip()) > 0:
                            u = PitchUpload(phase=phase,
                                            prompt=prompt)
                            u.save()

                    else:
                    
                        #check if existing upload has been edited
                        u = PitchUpload.objects.get(id=id)
                        if len(prompt.strip()) == 0:
                            u.delete()
                        elif u.prompt != prompt:
                            u.prompt = prompt
                            u.save()
                        
            except: pass

        setup = phase.setup_steps()
        setup.application_setup = True
        setup.save()

        return HttpResponseRedirect("/dashboard/phase/%s/" % phase_id)

    
    #this is pretty hacky, but it lets us include the standard
    #question editing chunk to clone for new entries by mimicking
    #the list[i].id format
    new_questions = [ { "id": "new", "max_points": 0 } ]

    return render_to_response('dashboard/edit_application.html', locals())



MONTH_NUMS = { "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
               "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12 }


#edit phases
@login_required
def edit_phases(request, competition_id):

    if not has_dash_perms(request, competition_id):
       return HttpResponseRedirect("/no_permissions/")

    editing_phase = int(request.GET.get("open", 0))

    competition = get_object_or_404(Competition, id=competition_id)

    if request.method == "POST":

        try: phase = Phase.objects.get(id=request.POST.get("phase_id", None))
        except:
            if "new_phase" in request.POST:
                phase = Phase(competition=competition)

        if phase:
            form = PhaseForm(request.POST, instance=phase)
            form.save()

            phase.is_deleted = request.POST.get("is_deleted") == "on"
            phase.save()

        if not competition.current_phase:
            competition.current_phase = phase
            competition.save()

        if competition.current_phase.is_deleted:
            competition.current_phase = competition.phases()[0]
            competition.save()

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
                
        if editing_phase:
            #if editing a single phase
            
            #then we've accomplished the first todo for that phase! yay!
            phase.setup_steps().details_confirmed = True
            phase.setup_steps().save()

            #redirect back to that phase page
            #after saving
            return HttpResponseRedirect("/dashboard/phase/%s/" % editing_phase)
        else:
            #if editing the competition's phases all together, then stay on
            #the page for further editing & navigation
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

    competition = get_object_or_404(Competition, id=competition_id)
    phase = get_object_or_404(Phase, id=phase_id)

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
            invite = JudgeInvitation(competition=competition,
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
                print 'Couldnt find judged_answer score because: %s' % sys.exc_info()[0]
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
        
        return HttpResponseRedirect("/dashboard/setup/1/")

    else:
    
        competition = request.user.get_profile().competition()

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

