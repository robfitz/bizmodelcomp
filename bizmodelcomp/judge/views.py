from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from userhelper.util import got_ev_key
from judge.models import *



#basically the one-stop-shop for judging. You come here and either log in
#or start having applications thrown at you to judge
def dashboard(request):

    #if they got to the judging page from the email link,
    #we can verify their email right now
    got_ev_key(request.GET.get("ev", False))
    
    #not logged it
    if not request.user.is_authenticated():

        print '/judge not authenticated'
        
        #redirect to judge login
        return HttpResponseRedirect('/accounts/register/?next=/judge/')

    #logged in
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

        #yes?
        else:
            
            #arbitrarily pick the first competition
            #TODO: handle judging multiple contests
            competition = judge_invites[0].competition

            #judging open in current phase?
            if competition.is_judging_open():

                if request.method == "POST":

                    for key in request.POST:

                        if key.startswith("answer_"):

                            answer_id = int(key[len("answer_"):])

                            answer = PitchAnswer.objects.get(id=question_id)
                            #TODO: BOOBS
                    

                #get a pitch to judge
                pitches = competition.current_phase().pitch_set.all()
                pitch = pitches[0]

                questions = pitch.phase.questions()
                uploads = pitch.phase.uploads()

                for question in questions:
                    try: question.answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question)
                    except: question.answer = None
                        
                for upload in uploads:
                    try: upload.file = PitchFile.objects.filter(pitch=pitch).get(upload=upload)
                    except: upload.file = None

                scores = range(1,100)
                
                #yeah! start showing shit!
                return render_to_response('judge/dashboard.html', locals())

            else:
                #no? tell them when judging opens
                message = """Hello,

Judging for this phase isn't open yet.

You'll receive an email as soon as the applications are ready for review.

Thanks!"""
                
                return render_to_response('util/message.html', locals())

    #should have already returned
    pass

