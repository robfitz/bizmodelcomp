from competition.models import *

def create_team_models():

    pitches = Pitch.objects.all()
    #change pitch.owner to a pitch.team.owner 
    for pitch in pitches:
        owner = pitch.owner
        #init new one-man team for owner
        team = Team(owner=pitch.owner, name="")
        team.save()
        #connect the team with their pitch
        pitch.team = team
        pitch.save()

        #special case: if pitch is form the echallenge comp, we have some extra data
        if pitch.phase.competition.hosted_url == "echallenge":
            try:
                #on some applications, we have already asked for the team name. grab it if it's there!
                team.name = PitchAnswer.objects.get(pitch=pitch, question__prompt="Team or Company Name").answer
                team.save()
            except: pass

            extra_role = ExtraFounderQuestion(prompt="Role at the university", raw_choices="Undergrad\nPostgrad\nAlumni\nStaff")
            extra_role.save()
            extra_affiliation = ExtraFounderQuestion(prompt="Affiliated university", raw_choices="UCL\nLBS\nRVC\nBirkbeck")
            extra_affiliation.save()

            #save extra info for primary founder
            try:
                answer = PitchAnswer.objects.get(pitch=pitch, question__prompt="Primary Contact's Role").answer
                extra = ExtraFounderInfo(question=extra_role, founder=team.owner, answer=answer)
                extra.save()
            except: pass

            try:
                answer = PitchAnswer.objects.get(pitch=pitch, question__prompt="Primary Contact Affiliation").answer
                extra = ExtraFounderInfo(question=extra_affiliation, founder=team.owner, answer=answer)
                extra.save()
            except: pass

            try:
                name = PitchAnswer.objects.get(pitch=pitch, question__prompt="Primary Contact Person").answer
                team.owner.name = name
                team.owner.save()
            except: pass


#there's more potential team data we can grab here, but since we're missing the email addresses it's all
#going to be meaningless and we won't have a good way to merge it with real founder accounts later
#
#                try:
#                    #then we've potentially got a bunch of extra founder infos
#                    extra_founder_answers = PitchAnswer.objects.filter(Q(pitch=pitch) & (Q(question__prompt="Additional Team Member Names & Affiliations") | Q(question__prompt="Team Member") ) )
#
#                    extra_role_answers = PitchAnswer.objects.filter(Q(pitch=pitch) & Q(question__prompt="Role") )
#
#                    extra_affil_answers = PitchAnswer.objects.filter(Q(pitch=pitch) & Q(question__prompt="Affiliation") )
