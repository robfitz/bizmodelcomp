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

    for pitch in competition.pitches():

        pitch.team_name = PitchAnswer.objects.filter(pitch=pitch).get(question__id=1).answer
        pitch.primary_name = PitchAnswer.objects.filter(pitch=pitch).get(question__id=2).answer

    return render_to_response('export/scores.csv', locals(), mimetype="text/csv")

    
