from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from userhelper.util import got_ev_key
from judge.models import *
from judge.util import get_next_pitch_to_judge
from competition.models import *



#basically the one-stop-shop for judging. You come here and either log in
#or start having applications thrown at you to judge
def dashboard(request):

    #if they got to the judging page from the email link,
    #we can verify their email right now
    got_ev_key(request.GET.get("ev", False))

    is_organizer = False
    competition = None
    
    #not logged it
    if not request.user.is_authenticated():

        print '/judge not authenticated'

        e = request.GET.get("e", "")

        account_page = "register"
        if e != "":
            if len(User.objects.filter(email=e)) > 0:
                #if there's already a user registered with the email
                #we're clicking to, direct them to login. otherwise
                #go to register
                account_page = "login"
        
        #redirect to judge login
        return HttpResponseRedirect('/accounts/%s/?next=/judge/&e=%s' % (account_page, e))

    #logged in, not organizer
    else:

        print '/judge is authenticated'
        
        #judgeinvites for this user?
        judge_invites = JudgeInvitation.objects.filter(user=request.user)

        print 'judge invites: %s' % judge_invites

        #no? redirect to no_permissions
        if len(judge_invites) == 0:

            judge_invites = JudgeInvitation.objects.filter(email=request.user.email)
            if len(judge_invites) > 0:

                invite = judge_invites[0]
                invite.user = request.user
                invite.save()

            else:

                return HttpResponseRedirect('/no_permissions/')

        #arbitrarily pick the first competition
        #TODO: handle judging multiple contests
        judge = judge_invites[0]
        competition = judge.competition

        if competition.owner == judge.user:
            is_organizer = True

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
            
            
            for key in request.POST:

                print 'found key in post: %s' % key
                
                if key.startswith("answer_"):

                    print 'FOUND JUDGE ANSWER: ' 

                    try:
                        score = int(request.POST[key])
                    except:
                        #this happens when there was no submitted answer, so,
                        #they loooose.
                        score = 0
                        
                    answer_id = int(key[len("answer_"):])
                    answer = PitchAnswer.objects.get(id=answer_id)

                    print 'score: %s, id: %s' % (score, answer_id)

                    try:
                        judged_answer = JudgedAnswer.objects.filter(judged_pitch=judgement).get(answer=answer)
                        judged_answer.score = score
                    except:
                        judged_answer = JudgedAnswer(judged_pitch=judgement,
                                                     answer=answer,
                                                     score=score)
                    judged_answer.save()
            

        #get a pitch to judge
        pitch = get_next_pitch_to_judge(competition, judge)

        if pitch:
            #populate forms
            questions = pitch.phase.questions()
            uploads = pitch.phase.uploads()

            for question in questions:
                print 'found question: %s' % question
                print 'pitch: %s' % pitch
                print 'pitch answers: %s' % PitchAnswer.objects.filter(pitch=pitch)
                try:
                    question.answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)
                    print 'found answer: %s' % question.answer
                except: question.answer = None
                    
            for upload in uploads:
                try: upload.file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
                except: upload.file = None

            scores = range(1,100)
            
            #yeah! start showing shit!
            return render_to_response('judge/dashboard.html', locals())

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

