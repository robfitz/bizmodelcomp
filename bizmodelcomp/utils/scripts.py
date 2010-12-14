from utils.util import rand_key
import random

from competition.models import *
from judge.models import *



LOREM = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""



def get_random_judge(phase):
    
    return random.choice(phase.judges())



def get_random_score(question):
    
    score = random.normalvariate((question.max_points + 1) / 2, question.max_points / 4)
    if score < 1: return 1
    elif score > question.max_points: return question.max_points
    else: return int(score)
    
    

def create_dummy_competition(user):

    #find unique hosted url
    url = None
    while True:
        url = rand_key(6)
        try:
            Competition.objects.get(hosted_url=key)
        except:
            break

    #create competition
    competition = Competition(owner=user,
            hosted_url=url,
            name="Lorem Ipsum",
            website="http://loremipsum.com")
    competition.save()

    #set as primary for this user so we see it in dashboard
    user.get_profile().selected_competition = competition
    user.get_profile().save()

    #create default phase
    phase = Phase(competition=competition,
            name="Phase 1")
    phase.save()
    competition.current_phase = phase
    competition.save()

    #a second, emptier phase
    phase = Phase(competition=competition,
            name="Phase 2")
    phase.save() 

    #add a few questions
    for i in range(1, 5):
        question = PitchQuestion(order=i,
                phase=competition.current_phase,
                prompt=LOREM[:50])
        question.save()

    #some judges
    for i in range(1, 5):
        judge = JudgeInvitation(competition=competition,
                email="judge_%s@example.com" % i,
                has_received_invite_email=True)
        judge.save()

    #create a bunch of applicants
    for i in range(1, 100):

        #TODO: properly avoid collisions
        email_num = rand_key(12)

        #applicant
        founder = Founder(name="Founder %s" % i,
                email = "%s@example.com" % email_num,
                phone = "1234567890",
                birth = "1900-01-28")
        founder.save()
        competition.applicants.add(founder)

        #application
        pitch = Pitch(owner=founder,
                phase=competition.current_phase,
                is_draft=False)
        pitch.save()
        
        #judging. we intentionally don't check for collisions
        #so that most apps will get judged twice, but not 100%
        judge_1 = get_random_judge(competition.current_phase)
        judge_2 = get_random_judge(competition.current_phase)

        judged = JudgedPitch(pitch=pitch,
                judge=judge_1)
        judged.save()

        #don't allow the same judge to rate the same app multiple times
        judged_2 = None
        if judge_1 != judge_2:
            judged_2 = JudgedPitch(pitch=pitch,
                    judge=judge_2)
            judged_2.save()
             
        #answers
        for q in competition.current_phase.questions():
            answer = PitchAnswer(question=q,
                    pitch=pitch,
                    answer=LOREM)
            answer.save()
               
            #judged answers
            j_answer = JudgedAnswer(judged_pitch=judged,
                    score=get_random_score(q),
                    answer=answer)
            j_answer.save()

            if judged_2:
                j_answer = JudgedAnswer(judged_pitch=judged_2,
                    score=get_random_score(q),
                    answer=answer)
                j_answer.save()

    #setup steps
    steps = competition.current_phase.setup_steps()
    steps.details_confirmed = True
    steps.application_setup = True
    steps.announced_applications = True
    steps.invited_judges = True
    steps.announced_judging_open = True
    steps.save()

    competition.save()

    return competition



def create_dummy_pitches_for_live_phase(from_phase_id, to_phase_id):

    online = Phase.objects.get(id=from_phase_id)
    live = Phase.objects.get(id=to_phase_id)

    if Pitch.objects.filter(phase=live).count() != 0:

        print 'ERROR: live phase already has pitches. Please delete them manually before using this script, since we dont want to double-create the pitches'
        return

    for pitch in Pitch.objects.filter(phase=online):
        dummy_pitch = Pitch(team=pitch.team,
                phase=live,
                order=pitch.order)
        dummy_pitch.save()

    print '%s created successfully' % Pitch.objects.filter(phase=live).count()
