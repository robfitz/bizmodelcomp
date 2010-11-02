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

        names = ''
        roles_and_affiliations = ''
        questions = PitchQuestion.objects.filter(phase=phase)

        i = 1
        while i <= 15:
            question = questions[i]
            answer = PitchAnswer.objects.filter(pitch=pitch).get(question=question).answer
            if i % 3 == 1: #name
                if answer and answer != '':
                    names = names + answer + '\\n'
            elif i % 3 == 2: #affiliation
                if answer and answer != '' and answer != '<affiliation>':
                    roles_and_affiliations = roles_and_affiliations + answer
            elif i % 3 == 0: #role
                if answer and answer != '' and answer != '<role>':
                    roles_and_affiliations = roles_and_affiliations + ' ' + answer + ' \\n'
                    
        

    return render_to_response('export/scores.csv', locals(), mimetype="text/csv")

    
