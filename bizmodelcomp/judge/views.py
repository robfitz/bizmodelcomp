from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from judge.models import *


#basically the one-stop-shop for judging. You come here and either log in
#or start having applications thrown at you to judge
def dashboard(request):

    #not logged it
    if not request.user.is_authenticated():
        
        #redirect to judge login
        return HttpResponseRedirect('/accounts/login/?next=/judge')

    #logged in
    else:
        
        #judgeinvites for this user?
        judge_invites = JudgeInvitation.objects.filter(user=request.user)

        #no? redirect to no_permissions
        if len(judge_invites) == 0:

            return HttpResponseRedirect('/no_permissions/')

        #yes?
        else:
            
            #arbitrarily pick the first competition
            #TODO: handle judging multiple contests
            competition = judge_invites[0].competition

            #judging open in current phase?
            if competition.is_judging_open():
                #yeah! start showing shit!
                return render_to_response('judge/dashboard.html')

            else:
                #no? tell them when judging opens
                message = """ """
                return render_to_response('util/message.html')

    #should have already returned
    pass

