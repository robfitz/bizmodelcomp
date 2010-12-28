from competition.models import Competition

#permissions helper
def has_dash_perms(request, competition_id):

    if not request.user.is_authenticated():
        return False

    try:
        competition = Competition.objects.get(id=competition_id)
        return competition.owner == request.user
    
    except:
        return False
    
    return False



def get_feedback_for_question(question_id, pitch):

    feedback = ""

    for judged_answer in JudgedAnswer.objects.filter(answer__question__id=question_id).filter(answer__pitch__team=pitch.team):
        if judged_answer and judged_answer.feedback:
            feedback = """%s%s

""" % (feedback, judged_answer.feedback.strip())

    return feedback

