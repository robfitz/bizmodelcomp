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

    if request.method == "GET":

        selected_phases = []

        view = request.GET.get("view")

        if view == "all_pitches":

            for phase in competition.phases():

                if request.GET.get("phase_%s" % phase.phase_num()):
                    selected_phases.append(phase)

            if len(selected_phases) == 0:

                selected_phases = competition.phases()

            header, rows = all_judges_table(selected_phases)
            print '****'
            print header
            print rows
            print ''

    print header
    for row in rows:
        print row

    return render_to_response('analytics/dashboard.html', locals())


def all_judges_table(phases):

    teams = []
    header = []
    rows = []

    header = ["Team"]
    for phase in phases:
        header.extend( [ "Phase %s pitch" % phase.phase_num(), "Phase %s judgements" % phase.phase_num(), "Phase %s average" % phase.phase_num() ] )
    header.append("Total score")

    for phase in phases:
        #first collect all the teams
        pitches = phase.all_pitches().all()
        for pitch in pitches:
            if pitch.team not in teams:
                teams.append(pitch.team)

    for team in teams:
        total_score = 0
        new_row = [team.name]
        #then add the phases as columns
        for phase in phases:
            try:
                pitch = Pitch.objects.get(team=team, phase=phase)
                new_row.append("<a href='/dashboard/pitch/%s/'>View</a>" % pitch.id)
                judgement_list = ""
                for judgement in JudgedPitch.objects.filter(pitch=pitch):
                    judgement_list += "<a href='/dashboard/judgement/%s/'>%s</a><br/>" % (judgement.id, judgement.score())
                new_row.append(judgement_list)
                new_row.append("%s" % pitch.average_score())
                total_score += pitch.average_score()

            except:
                #three blank table cells
                new_row.extend( [ "", "", "" ] )

        new_row.append("%s" % total_score)
        rows.append(new_row)

    return header, rows

