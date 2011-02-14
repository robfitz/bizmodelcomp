from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from competition.models import *


@login_required
def dashboard(request, comp_url):

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    if competition.owner != request.user:
        return HttpResponseRedirect('/dashboard/')

    header = []
    rows = []
    view = None

    selected_phases = []

    if request.method == "GET":
        view = request.GET.get("view")

        for phase in competition.phases():
            if request.GET.get("phase_%s" % phase.phase_num()):
                selected_phases.append(phase)

        if len(selected_phases) == 0:
            selected_phases = competition.phases()

    return render_to_response('analytics/dashboard.html', locals())



def table(request, comp_url):

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    if competition.owner != request.user:
        return HttpResponseRedirect('/dashboard/')

    header = []
    rows = []
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
            header, rows = all_pitches_table(selected_phases)

        elif view == "all_judges":
            header, rows = all_judges_table(competition)
            html = "analytics/all_judges.html"

        elif view == "for_judge":
            judge_id = request.GET.get("judge")

            judge = JudgeInvitation.objects.get(id=judge_id)
            header, rows = pitches_for_judge_table(selected_phases, judge)
            html = "analytics/all_judges.html"

    return render_to_response("analytics/all_pitches.html", locals())


def all_judges_table(competition):

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
                    total_score = total_score + j.score()

                row.append( len(judgements) )
                if len(judgements) == 0:
                    row.append("-")
                else:
                    row.append("%s" % (total_score / len(judgements) ) )

        rows.append(row)

    return header, rows
                

def pitches_for_judge_table(phases, judge):

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
                row.append( "<a href='javascript:void(0);' onclick=\"popup('/dashboard/judgement/%s/');\">%s</a>" % (judgement.id, judgement.score() ) )

            except:
                row.append( "-" )

        rows.append(row)

    return header, rows



def all_pitches_table(phases):

    teams = []
    header = ["<input id='check_select_all' type='checkbox' href='javascript:void(0);' onclick=\"$(\'.checkbox\').attr(\'checked\', $(\'#check_select_all\').attr(\'checked\'));\"></a>", "Team"]
    rows = []

    for phase in phases:
        header.extend( [ "Phase %s<br/>pitches" % phase.phase_num(), "Phase %s<br/>scores" % phase.phase_num(), "Phase %s<br/>average" % phase.phase_num() ] )
    header.append("Total score")

    for phase in phases:
        #first collect all the teams
        pitches = phase.all_pitches().all()
        for pitch in pitches:
            if pitch.team is not None and pitch.team not in teams:
                teams.append(pitch.team)

    for i, team in enumerate(teams):
        total_score = 0
        #add selection checkbox and team name

        team_name = unicode(team)
        #for tag in 
        
        new_row = []
        new_row.append("<input type='checkbox' id='checkbox_%s' class='checkbox' />" % i)
        new_row.append(team_name)

        #then add the phases as columns
        for phase in phases:
            try:
                pitch = Pitch.objects.get(team=team, phase=phase)
                new_row.append("<a href='javascript:void(0);' onclick=\"popup('/dashboard/pitch/%s/');\">View</a> (%s&#37;)" % (pitch.id, pitch.percent_complete()))
                judgement_list = ""
                for i, judgement in enumerate(JudgedPitch.objects.filter(pitch=pitch)):
                    if i > 0:
                        judgement_list += ", "
                    judgement_list += "<a href='javascript:void(0);' onclick=\"popup('/dashboard/judgement/%s/');\">%s</a>" % (judgement.id, judgement.score())
                new_row.append(judgement_list)
                new_row.append("%s" % pitch.average_score())
                total_score += pitch.average_score()

            except:
                #three blank table cells
                new_row.extend( [ "-", "-", "-" ] )

        new_row.append("%s" % total_score)
        rows.append(new_row)

    return header, rows

