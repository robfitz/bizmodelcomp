from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from userhelper.util import got_ev_key
from judge.models import *
from judge.util import get_next_pitch_to_judge
from competition.models import *
from competition.util import get_competition_for_user
from utils.util import ordinal


def get_permissions_redirect(request, competition):
    
    #not logged it
    if not request.user.is_authenticated():
        print 'not logged in'

        e = request.GET.get("e", "")

        account_page = "register"
        if e != "":
            if len(User.objects.filter(email=e)) > 0:
                #if there's already a user registered with the email
                #we're clicking to, direct them to login. otherwise
                #go to register
                account_page = "login"
        
        #redirect to judge login
        return '/accounts/%s/?next=/judge/&e=%s' % (account_page, e)

    #logged in, not organizer
    else:
        print 'logged in'
        
        #judgeinvites for this user?
        judge_invites = JudgeInvitation.objects.filter(user=request.user)
        print 'invites %s' % judge_invites

        #no? redirect to no_permissions
        if len(judge_invites) == 0:
            print 'no judge invites for user'

            judge_invites = JudgeInvitation.objects.filter(email=request.user.email)
            if len(judge_invites) > 0:
                print 'found judge invite for email'

                #TODO: handle multiple competitions
                invite = judge_invites[0]
                invite.user = request.user
                invite.save()

            elif request.user == competition.owner:
                print 'creating judge invite for owner'
                
                #if it's an organizer trying to judge, we'll make
                #a judge entry for them, since they should always
                #have one
                invite = JudgeInvite(competition=competition,
                                     email=request.user.email,
                                     user=request.user,
                                     has_received_invite_email=True) #don't sent them another
                invite.save()
                
            else:
                return '/no_permissions/'

        return None

@login_required
def dashboard(request):

    #if they got to the judging page from the email link,
    #we can verify their email right now
    got_ev_key(request.GET.get("ev", False))
    
    competition = get_competition_for_user(request.user)
    is_organizer = competition.owner == request.user
    
    redirect = get_permissions_redirect(request, competition)
    if redirect:
        return HttpResponseRedirect(redirect)
    
    try:
        #if a judge thing exists for this user, grab it
        judge = JudgeInvitation.objects.filter(user=request.user)[0]
    except:
        fail = None
        fail.no_judge_invite()

    judged_pitches = competition.current_phase.judgements(judge)
    num_judged = len(judged_pitches)
    num_to_judge = len(competition.current_phase.pitches_to_judge(judge))
    judge_rank = competition.current_phase.judge_rank(judge)

    max_score = competition.current_phase.max_score()
    step_size = max(max_score / 20, 1)
    score_groups = []

    for judged_pitch in judged_pitches:
        score = judged_pitch.score()
        step = int(score / step_size) * step_size

        for group in score_groups:
            if group['score'] == step:
                group['quantity'] += 1
                break
        else:
            score_groups.append({ 'score': step, 'quantity': 1 })

    print score_groups

    phase = competition.current_phase

    return render_to_response('judge/dashboard.html', locals())



#basically the one-stop-shop for judging. You come here and either log in
#or start having applications thrown at you to judge
@login_required
def judging(request, judgedpitch_id=None):

    #if we're requesting a specific pitch, only allow it for
    #either the organizer or the person who did the judging
    judged_pitch = None
    if judgedpitch_id is not None:
        judged_pitch = get_object_or_404(JudgedPitch, id=judgedpitch_id)
        if judged_pitch.judge.user != request.user and request.user != judged_pitch.pitch.phase.competition.owner:
            return HttpResponseRedirect('/no_permissions/')
        
    
    competition = get_competition_for_user(request.user)
    is_organizer = competition.owner == request.user

    redirect = get_permissions_redirect(request, competition)
    if redirect:
        return HttpResponseRedirect(redirect)
    
    try:
        #if a judge thing exists for this user, grab it
        judge = JudgeInvitation.objects.filter(user=request.user)[0]
    except:
        fail = None
        fail.no_judge_invite()

    #judging open in current phase?
    if competition and competition.is_judging_open():
        
        if request.method == "POST":
            
            pitch_id = request.POST["pitch"]
            pitch = Pitch.objects.get(id=pitch_id)
            
            try:
                #look for existing judgement
                judgement = JudgedPitch.objects.filter(pitch=pitch).get(judge=judge)
            
            except:
                #create new judgement
                judgement = JudgedPitch(judge=judge,
                                        pitch=pitch)
                judgement.save()

            if "feedback" in request.POST:

                judgement.feedback = request.POST["feedback"]
                judgement.save()

            if "overall_score" in request.POST:

                judgement.overall_score = request.POST["overall_score"]
                judgement.save()
            
            
            for key in request.POST:

                if key.startswith("answer_"):

                    try:
                        score = int(request.POST[key])
                    except:
                        #this happens when there was no submitted answer, so,
                        #they loooose.
                        score = 0
                        
                    answer_id = int(key[len("answer_"):])
                    answer = PitchAnswer.objects.get(id=answer_id)

                    try:
                        judged_answer = JudgedAnswer.objects.filter(judged_pitch=judgement).get(answer=answer)
                        judged_answer.score = score
                    except:
                        judged_answer = JudgedAnswer(judged_pitch=judgement,
                                                     answer=answer,
                                                     score=score)
                    judged_answer.save()

            #keep page refresh clean of POST data
            if judged_pitch is not None:
                return HttpResponseRedirect('/judge/')
            else:
                return HttpResponseRedirect('/judge/go/')

        #get a pitch to judge
        if judged_pitch is not None:
            pitch = judged_pitch.pitch
        else:
            pitch = get_next_pitch_to_judge(competition, judge)

        if pitch:
            #populate forms
            questions = pitch.phase.questions()
            uploads = pitch.phase.uploads()

            for question in questions:
                try:
                    question.answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)

                    if judged_pitch is not None:

                        try:
                            question.score = JudgedAnswer.objects.filter(judged_pitch=judged_pitch).get(answer=question.answer).score
                        except:
                            question.score = ""

                except:
                    question.answer = None

            for upload in uploads:
                try: upload.file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
                except: upload.file = None

            scores = range(1,100)

            num_judged = len(competition.current_phase.judgements(judge))
            num_to_judge = len(competition.current_phase.pitches_to_judge(judge))
            judge_rank = competition.current_phase.judge_rank(judge)
            
            #yeah! start showing shit!
            return render_to_response('judge/judging.html', locals())

        else:
            message = """Judging is complete and all applications have already been assessed.

Thanks for your help!"""

            return render_to_response('util/message.html', locals())

    else:
        #no? tell them when judging opens
        message = """Hello,

Judging for this phase isn't open yet.

You'll receive an email as soon as the applications are ready for review.

Thanks!"""
        
        return render_to_response('util/message.html', locals())

    #should have already returned
    pass

