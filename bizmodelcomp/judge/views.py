import sys

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from userhelper.util import got_ev_key
from userhelper.models import UserProfile
from judge.models import *
from judge.util import get_next_pitch_to_judge
from competition.models import *
from competition.util import get_competition_for_user
from utils.util import ordinal
import charts.util as chart_util
from sitecopy.models import SiteCopy



@login_required
def list(request, comp_url):
    
    competition = get_object_or_404(Competition, hosted_url=comp_url)

    redirect = get_permissions_redirect(request, competition)
    if redirect:
        return HttpResponseRedirect(redirect)

    judged = []
    unjudged = []
    
    for pitch in competition.current_phase.pitches(-1):

        #figure if i've judged this one yet or not
        judgements = JudgedPitch.objects.filter(pitch=pitch).filter(judge__user=request.user)
        
        if judgements.count() == 0:
            unjudged.append(pitch)
        else:
            pitch.judgement = judgements[0]
            judged.append(pitch)

    num_judged = len(judged)
    num_to_judge = len(unjudged)

    #cleanup of local vars so header displays properly
    pitch = None

    return render_to_response('judge/list.html', locals())



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
                invite = JudgeInvitation(competition=competition,
                                     email=request.user.email,
                                     user=request.user,
                                     has_received_invite_email=True) #don't sent them another
                invite.save()
                
            else:
                return '/no_permissions/'

        return None

@login_required
def dashboard(request, comp_url=None):

    #if they got to the judging page from the email link,
    #we can verify their email right now
    got_ev_key(request.GET.get("ev", False))
    
    #intro text to help judge know what to do
    intro = ""
    try:
        intro = SiteCopy.objects.get(id="intro_judge")
    except:
        pass
    
    competition = None
    if comp_url is not None:
        competition = get_object_or_404(Competition, hosted_url=comp_url)
    else:
        competition = get_competition_for_user(request.user)

    is_organizer = competition is not None and competition.owner == request.user
    
    redirect = get_permissions_redirect(request, competition)
    if redirect:
        return HttpResponseRedirect(redirect)
    
    try:
        #if a judge thing exists for this user, grab it
        judge = JudgeInvitation.objects.filter(user=request.user)[0]
    except:
        fail = None
        fail.no_judge_invite()

    judged_pitches = competition.current_phase.judgements(judge, -1)
    num_judged = len(judged_pitches)
    num_to_judge = len(competition.current_phase.pitches_to_judge(judge, -1))

    print 'dashboard, judged=%s, to judge=%s' % (num_judged, num_to_judge)
    judge_rank = competition.current_phase.judge_rank(judge)

    max_score = competition.current_phase.max_score()
    score_groups = chart_util.score_distribution(competition.current_phase.judgements(), max(max_score / 20, 1))
    my_score_groups = chart_util.score_distribution(judged_pitches, max(max_score / 20, 1))

    phase = competition.current_phase

    return render_to_response('judge/dashboard.html', locals())



#basically the one-stop-shop for judging. You come here and either log in
#or start having applications thrown at you to judge
@login_required
def judging(request, comp_url=None, judgedpitch_id=None, unjudged_pitch_id=None):

    competition = None
    if comp_url:
        competition = get_object_or_404(Competition, hosted_url=comp_url)
    elif judgedpitch_id:
        judgedpitch = get_object_or_404(JudgedPitch, id=judgedpitch_id)
        competition = judgedpitch.pitch.phase.competition
    elif unjudged_pitch_id is not None:
        pitch = get_object_or_404(Pitch, id=unjudged_pitch_id)
        competition = pitch.phase.competition
    else:
        competition = get_competition_for_user(request.user)

    judging_criteria = competition.current_phase.judgingcriteria_set.all()

    try:
        request.user.get_profile()
    except:
        #ensure old users have a profile
        profile = UserProfile(user=request.user)
        profile.save()

    judged_pitch = None
    pitch = None

    #if we're requesting a specific pitch, only allow it for
    #either the organizer or the person who did the judging
    if judgedpitch_id is not None:

        judged_pitch = get_object_or_404(JudgedPitch, id=judgedpitch_id)

        if judged_pitch.judge.user != request.user and request.user != judged_pitch.pitch.phase.competition.owner:
            return HttpResponseRedirect('/no_permissions/')

    elif unjudged_pitch_id is not None:

        pitch = get_object_or_404(Pitch, id=unjudged_pitch_id)

        competition = pitch.phase.competition

        #they're allowed to judge this particular application if they're either a judge
        #or the owner of this competition
        if request.user != competition.owner and JudgeInvitation.objects.filter(user=request.user).filter(competition=competition):

            #if they've already judged this application, we want to redirect them to
            #the edit page (which ends up in the same place for now, but it may not always)
            earlier_pitches = JudgedPitch.objects.filter(pitch=pitch, judge__user=request.user)
            if earlier_pitches.count() > 0:

                return HttpResponseRedirect('/judge/review/%s/' % earlier_pitches[0].id)

    
    is_organizer = competition.owner == request.user

    redirect = get_permissions_redirect(request, competition)
    if redirect:
        return HttpResponseRedirect(redirect)
    
    try:
        #if a judge thing exists for this user, grab it
        judge = JudgeInvitation.objects.get(user=request.user, competition=competition)
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
                judgement = JudgedPitch.objects.filter(pitch=pitch, judge=judge)[0]
                print 'saving score, found judgement: %s' % judgement
            
            except:
                #create new judgement
                judgement = JudgedPitch(judge=judge,
                                        pitch=pitch)
                judgement.save()
                print 'saving score, created new judgement: %s' % judgement
            
            for key in request.POST:

                print 'saving score: key=%s, val=%s' % (key, request.POST.get(key))

                if key.startswith("score_") or key.startswith("feedback_"):

                    criteria = None

                    try:
                        toks = key.split('_')
                        criteria_id = int(toks[len(toks) - 1]) #last token is ID
                        print '  criteria id: %s' % criteria_id
                        criteria = JudgingCriteria.objects.get(id=criteria_id)
                        print '  criteria: %s' % criteria
                    except:
                        print '  except: %s' % sys.exc_info()[0]
                        #can't save the score if we don't find a valid criteria id
                        continue

                    try:
                        #judged_answer = JudgedAnswer.objects.filter(judged_pitch=judgement).get(answer=answer)
                        judged_answer = JudgedAnswer.objects.filter(judged_pitch=judgement).get(criteria=criteria)
                        print '  found judged answer: %s' % judged_answer
                    except:
                        judged_answer = JudgedAnswer(judged_pitch=judgement,
                                                     criteria=criteria)
                        judged_answer.save()

                        print '  created new judged answer: %s' % judged_answer

                    if key.startswith("score_"):

                        try:
                            judged_answer.score = int(request.POST.get(key, 0))

                        except:
                            #this happens when there was no submitted answer, so
                            #they loooose.
                            judged_answer.score = 0

                    elif key.startswith("feedback_"):
                        judged_answer.feedback = request.POST.get(key)

                    judged_answer.save()

            if pitch.phase.pitch_type == "live pitch":
                #judging live we always go back to the list so they can be sure
                #to pick the correct next pitch
                return HttpResponseRedirect('/judge/%s/list/' % competition.hosted_url)

            elif judgedpitch_id is not None or unjudged_pitch_id is not None:
                #judging online phases, we go back to the list if they have
                #already started choosing specific pitches
                return HttpResponseRedirect('/judge/%s/list/' % competition.hosted_url)

            else:
                #if they're judging online ptiches and going via the "go"
                #option, we just keep feeding them more relevant pitches
                return HttpResponseRedirect('/judge/%s/go/' % competition.hosted_url)

        #get a pitch to judge
        if judged_pitch is not None:
            pitch = judged_pitch.pitch
        elif not pitch:
            pitch = get_next_pitch_to_judge(competition, judge)

        if pitch:
            #populate forms
            questions = pitch.phase.questions()
            uploads = pitch.phase.uploads()

            for question in questions:
                try:
                    question.answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)
                except:
                    question.answer = None

            for criteria in judging_criteria:
                try:
                    print 'trying to get judged_answer for criteria: %s' % criteria
                    judged_answer = JudgedAnswer.objects.get(criteria=criteria,
                            judged_pitch=judged_pitch)
                    print '  got answer: %s' % judged_answer
                    criteria.answer = judged_answer
                    print '  set as criteria.answer'
                except:
                    print '  exception: %s' % sys.exc_info()[0]
                    criteria.answer = None

            for upload in uploads:
                try: upload.file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
                except: upload.file = None

            scores = range(1,100)

            max_score = competition.current_phase.max_score()
            print 'maxscore: %s' % max_score
    
            num_judged = len(competition.current_phase.judgements(judge, -1))
            num_to_judge = len(competition.current_phase.pitches_to_judge(judge, -1))
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

