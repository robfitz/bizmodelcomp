from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from competition.models import *
from judge.models import *



@login_required
def scores_csv(request, phase_id, verbose_scores=False):

    phase = Phase.objects.get(id=phase_id)
    competition = phase.competition
    
    #organizer permissions?
    if request.user != competition.owner:

        return HttpResponseRedirect('/no_permissions/')

    pitches = competition.pitches()
    for pitch in pitches:
        
        try: pitch.team_name = ''.join(PitchAnswer.objects.filter(pitch=pitch).get(question__id=1).answer.split(','))
        except: pass
        
        try: pitch.primary_name = ''.join(PitchAnswer.objects.filter(pitch=pitch).get(question__id=2).answer.split(','))
        except: pass

    return render_to_response('export/scores.csv', locals(), mimetype="text/csv")

    
