from django.db import connection

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from competition.models import *



def table(request, comp_url):

    print 'analytics.views.table()'

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    if competition.owner != request.user:
        return HttpResponseRedirect('/dashboard/')

    phases = competition.all_phases.select_related("pitch_set")

    header = []
    rows = []
    teams = []
    view = None

    html = "analytics/all_pitches.html"

    if request.method == "GET":

        selected_phases = []

        view = request.GET.get("view")

        #it's common for tables to be customizable on which phases, so keep that general
        for phase in competition.phases():
            if request.GET.get("phase_%s" % phase.phase_num()):
                selected_phases.append(phase)

        if len(selected_phases) == 0:
            selected_phases = competition.phases()

        if view == "all_pitches":
            print "analytics.table() [teams] *** __%s__ *** query count" % len(connection.queries)
            teams = all_pitches_table(selected_phases)
            #header, rows = all_pitches_table(selected_phases)

        elif view == "all_judges":
            print "analytics.table() [judges] *** __%s__ *** query count" % len(connection.queries)
            header, rows = all_judges_table(competition)
            html = "analytics/all_judges.html"

        elif view == "for_judge":
            judge_id = request.GET.get("judge")

            judge = JudgeInvitation.objects.get(id=judge_id)
            header, rows = pitches_for_judge_table(selected_phases, judge)
            html = "analytics/all_judges.html"

    print "analytics.table() *** __%s__ *** query count" % len(connection.queries)
    response = render_to_response("analytics/all_pitches.html", locals())
    print "analytics.table() *** __%s__ *** query count" % len(connection.queries)
    return response


def all_judges_table(competition):

    print 'analytics.views.all_judges_table()'

    judges = []
    rows = []
    header = ["Judge"]
    for phase in Phase.objects.filter(competition=competition):
        header.extend( [ "Phase %s<br/>num judged" % phase.phase_num(), "Phase %s<br/>average" % phase.phase_num() ] )

    judges = JudgeInvitation.objects.filter(competition=competition)

    for judge in judges:

        row = ["<a href='/dashboard/data/%s/?view=for_judge&judge=%s'>%s</a>" % (competition.hosted_url, judge.id, judge) ]

        for phase in Phase.objects.filter(competition=competition):

            if judge.this_phase_only and judge.this_phase_only != phase:

                row.extend( [ "N/A", "N/A" ] )

            else:

                judgements = JudgedPitch.objects.filter(judge=judge).filter(pitch__phase=phase)
                total_score = 0
                for j in judgements:
                    total_score = total_score + j.score

                row.append( len(judgements) )
                if len(judgements) == 0:
                    row.append("-")
                else:
                    row.append("%s" % (total_score / len(judgements) ) )

        rows.append(row)

    return header, rows
                

def pitches_for_judge_table(phases, judge):

    print 'analytics.views.pitches_for_judge_table'

    teams = []
    header = ["Team"]
    rows = []

    for phase in phases:
        header.extend( [ "Phase %s judgement" % phase.phase_num() ] )

    for phase in phases:

        judgements = JudgedPitch.objects.filter(judge=judge).filter(pitch__phase=phase)

        for judgement in judgements:

            if judgement.pitch.team not in teams:

                teams.append(judgement.pitch.team)

    for team in teams:

        row = [ "%s" % team ]

        for phase in phases:

            try:
                judgement = JudgedPitch.objects.get(judge=judge, pitch__team=team, pitch__phase=phase)
                row.append( "<a href='javascript:void(0);' onclick=\"popup('/dashboard/judgement/%s/');\">%s</a>" % (judgement.id, judgement.score ) )

            except:
                row.append( "-" )

        rows.append(row)

    return header, rows



def all_pitches_table(phases):

    print 'analytics.views.all_pitches_table'

    teams = []

    pitches = Pitch.objects.filter(phase__in=phases).select_related("team", "phase", "judgements")

    #{ "team.id": {"pitch.id":pitch,...}, ...}
    dict = {}

    for pitch in pitches:
        if pitch.team and pitch.team not in teams:
            teams.append(pitch.team)
            dict[pitch.team.id] = {}
        if pitch and pitch.team and pitch.phase:
            dict[pitch.team.id][pitch.phase.id] = pitch

    for i, team in enumerate(teams):

        #to display in template
        team.pitches = []
        total_score = 0
        max_percent = 0

        #then add the phases as columns
        for phase in phases:

            try:
                pitch = dict[team.id][phase.id]
                #pitch = pitches.get(team=team, phase=phase)

                #team has participated in this phase, so show pitch info in template
                team.pitches.append(pitch)

                p = pitch.percent_complete() 
                if p > max_percent:
                    max_percent = p

                total_score += pitch.average_score

            except:
                #team not involved in this phase, render nothing in template
                team.pitches.append(None)

        team.total_score = total_score
        team.percent = int(max_percent)

    #return header, rows
    return teams

