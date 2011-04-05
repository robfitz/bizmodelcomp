from utils.util import rand_key
import random

from competition.models import *
from judge.models import *



def pitch_csv(hosted_url, question_ids, show_phone=False, show_uni=False, show_timestamp=False, show_scores=False, show_feedback=False):

  comp = Competition.objects.get(hosted_url=hosted_url)
  criteria = JudgingCriteria.objects.filter(phase=comp.current_phase).all()

  pitches = Pitch.objects.filter(phase=comp.current_phase).select_related("judgements")

  if question_ids == "all":
    questions = PitchQuestion.objects.filter(phase=comp.current_phase)

  for pitch in pitches:
    toks = [ unicode(pitch.team).decode('unicode-escape') ]
    toks.append(pitch.percent_complete())
    toks.append(pitch.team.owner.email)

    if show_phone: toks.append(pitch.team.owner.phone)
    if show_uni: toks.append(pitch.team.owner.institution)
    if show_timestamp: toks.append(pitch.created.isoformat())

    if question_ids == "all":
      for q in questions:
        try:
          answer = PitchAnswer.objects.get(question__id=q.id, pitch=pitch)
          toks.append(unicode(answer))
        except: toks.append("")
            
    else:
      for question_id in question_ids:
        try:
          answer = PitchAnswer.objects.get(question__id=question_id, pitch=pitch)
          toks.append(unicode(answer))
        except: toks.append("")

    if show_scores:
      tok = ""
      for judgement in pitch.judgements.all():
        if tok == "": tok = "%s" % judgement.score
        else: tok = "%s, %s" % (tok, judgement.score)
      toks.append(tok)
      toks.append("%s" % pitch.average_score)

    if show_feedback:
      for judgement in pitch.judgements.all():
        for feedback in judgement.judgedanswer_set.filter(criteria__is_text_feedback=True):
          toks.append(feedback.feedback)

    line = ""
    for token in toks:
      clean_tok = unicode(token).replace("^","").replace("\"", "'")
      clean_tok = '"%s"' % clean_tok
      line += unicode(clean_tok) + "^"
    print line



def judging_csv(hosted_url):

  comp = Competition.objects.get(hosted_url=hosted_url)
  criteria = JudgingCriteria.objects.filter(phase=comp.current_phase).all()

  judgements = JudgedPitch.objects.filter(pitch__phase__competition=comp)

  csv = ""
  for judgement in judgements:
    
    toks = []
    toks.append(unicode(judgement.pitch.team))
    toks.append(unicode(judgement.judge))
    toks.append(unicode(judgement.score))
    
    for c in criteria:
      score = JudgedAnswer.objects.get(judged_pitch=judgement, criteria=c)
      if not c.is_text_feedback:
        toks.append(unicode(score.score))
      else: toks.append(unicode(score.feedback))

    line = ""
    for token in toks:
      line += token.replace("^","") + "^"
    print line
    #csv += line

  #return csv



LOREM = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""



def get_random_judge(phase):
    
    return random.choice(phase.judges())



def get_random_score(criteria):
    
    score = random.normalvariate((criteria.max_points + 1) / 2, criteria.max_points / 4)
    if score < 1: return 1
    elif score > criteria.max_points: return criteria.max_points
    else: return int(score)
    
    

#phase 1: online pitch, already complete
#phase 2: online pitch, submissions in, judging partial
#phase 3: live pitch, setup complete but no pitches
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
            name="My fourth competition",
            website="http://myfirstcompetition.com")
    competition.save()

    #create default phase
    phase_1 = Phase(competition=competition,
            name="Phase 1",
            is_judging_enabled=False)
    phase_1.save()

    #a second, emptier phase
    phase_2 = Phase(competition=competition,
            name="Phase 2",
            is_judging_enabled=True)
    phase_2.save() 

    #a third, live and incomplete phase
    phase_3 = Phase(competition=competition,
            name="Phase 3")
    phase_3.save() 

    competition.current_phase = phase_2
    competition.save()

    #add a few questions.
    #on phase 1 & 2 (online) you have 4 questions that 
    #are scored normally, and then one open feedback spot
    for i in range(1, 5):
        question = PitchQuestion(order=i,
                phase=phase_1,
                prompt=LOREM[:50],
                max_points=10)
        
        ## REMOVE - Questions no longer feedback prompts
        #if i == 4:
        #    question.judge_feedback_prompt = "Overall thoughts?"
        #    question.is_hidden_from_applicants = True
        #
        question.save()

        question = PitchQuestion(order=i,
                phase=phase_2,
                prompt=LOREM[:50],
                max_points=10)
       ## REMOVE - Questions no longer feedback prompts
       # if i == 4:
       #     question.judge_feedback_prompt = "Overall thoughts?"
       #     question.is_hidden_from_applicants = True
        question.save()

    #add judging criteria for first phase
    
    for i in range(1, 5):
        criteria = JudgingCriteria(phase=phase_1,
                order=i,
                prompt=LOREM[:11],
                max_points=10, is_text_feedback=False)
        criteria.save()
    
    for i in range(1, 3):
        criteria = JudgingCriteria(phase=phase_1,
                order=i,
                prompt=LOREM[:11],
                is_text_feedback=True)
        criteria.save()
        
    #add judging criteria for second phase
    
    for i in range(1, 5):
        criteria = JudgingCriteria(phase=phase_2,
                order=i,
                prompt=LOREM[:11],
                max_points=10, is_text_feedback=False)
        criteria.save()
    
    for i in range(1, 3):
        criteria = JudgingCriteria(phase=phase_2,
                order=i,
                prompt=LOREM[:11],
                is_text_feedback=True)
        criteria.save()

    ## REMOVE - Questions no longer feedback prompts
    #
    #three open feedback questions for the live pitch
    #for i in range(1, 3):
    #    question = PitchQuestion(order=i,
    #            phase=phase_3,
    #            prompt=LOREM[:50],
    #            max_points=10,
    #            judge_feedback_prompt = LOREM[:20],
    #            is_hidden_from_applicants = True)
    #   question.save()

    #some judges
    for i in range(1, 5):
        judge = JudgeInvitation(competition=competition,
                email="judge_%s@example.com" % i,
                has_received_invite_email=True)
        judge.save()

    #create a bunch of applicants
    for i in range(1, 100):

        email_num = rand_key(12)

        #applicant
        founder = Founder(name="Founder %s" % i,
                email = "%s@example.com" % email_num,
                phone = "1234567890",
                birth = "1900-01-28")
        try:
            founder.save()
        except:
            continue

        competition.applicants.add(founder)

        team = Team(owner=founder,
                name="Team %s" % i)
        team.save()

        #answers, but only for the first 2 phases (3rd live phase hasn't been done yet!) 
        for phase in [phase_1, phase_2]:
            
            #application
            pitch = Pitch(team=team,
                    phase=phase,
                    is_draft=False)
            pitch.save()
            
            #judging. we intentionally don't check for collisions
            #so that most apps will get judged twice, but not 100%
            judge_1 = get_random_judge(phase)
            judge_2 = get_random_judge(phase)

            judged = JudgedPitch(pitch=pitch,
                    judge=judge_1)
            
            judged.save()

            #don't allow the same judge to rate the same app multiple times
            judged_2 = None
            if judge_1 != judge_2:
                judged_2 = JudgedPitch(pitch=pitch,
                        judge=judge_2)
                judged_2.save()
            
            
            #loop through all questions to answer and judge them
            for question in phase.questions():

                answer = None

                if not question.is_hidden_from_applicants:
                    #student can see the question, should answer it
                    answer = PitchAnswer(question=question,
                            pitch=pitch,
                            answer=LOREM)
                    answer.save()
            
            ##print 'Begin'
            ## TODO - Below sort out judging with JudgePitch and JudgeAnswer
            for criteria in phase.judging_criteria():
            
                ## Not sure why a bunch of the scores created are zero, tried checking if it was scoring the text feedback but didn't work
                ##if criteria.is_text_feedback==False:
                
                    j_answer = JudgedAnswer(judged_pitch=judged,
                            score=get_random_score(criteria),
                            answer=answer, criteria=criteria)
                    j_answer.save()
                    ##print j_answer
            
                    judged.calculate_cached_score()
                    ##print 'success'
            
                
                #judges always answer, one way or another. answer=Null mean
                #that the question was hidden from applicant and judges need leave feedback
                #j_answer = JudgedAnswer(judged_pitch=judged,
                #        score=get_random_score(question),
                #        answer=answer)
                #if question.judge_feedback_prompt:
                #    j_answer.feedback = LOREM
                #j_answer.save()

                #if judged_2:
                #    j_answer = JudgedAnswer(judged_pitch=judged_2,
                #        score=get_random_score(question),
                #        answer=answer)
                #    if question.judge_feedback_prompt:
                #        j_answer.feedback = LOREM
                #    j_answer.save()

    #setup steps - phase 1 done
    steps = phase_1.setup_steps()
    steps.details_confirmed = True
    steps.application_setup = True
    steps.announced_applications = True
    steps.invited_judges = True
    steps.announced_judging_open = True
    steps.selected_winners = True
    steps.save()

    #setup steps - phase 2 just needs winners declared
    steps = phase_2.setup_steps()
    steps.details_confirmed = True
    steps.application_setup = True
    steps.announced_applications = True
    steps.invited_judges = True
    steps.announced_judging_open = True
    steps.selected_winners = False
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
                owner=pitch.owner,
                phase=live,
                order=pitch.order)
        dummy_pitch.save()

    print '%s created successfully' % Pitch.objects.filter(phase=live).count()
