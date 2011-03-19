
def score_distribution(judged_pitches, step_size=1):

    score_groups = []
    
    for judged_pitch in judged_pitches:
        score = judged_pitch.score()
        step = int(score / step_size) * step_size

        for group in score_groups:
            if group['score'] == step:
                group['quantity'] += 1
                break
        else:
            score_groups.append({ 'score': step, 'quantity': 1 })

    return score_groups

