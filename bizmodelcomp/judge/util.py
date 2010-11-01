import random

def get_next_pitch_to_judge(competition, judge):

    #temp
    pitches = competition.current_phase().pitches_to_judge()
    index = random.randrange(0, len(pitches)-1)
    return pitches[index]

    #is judge an organizer? yes

        #get all pitches from this comp

        #get all pitches not yet judged by me

        #return one randomly

    #judge is NOT an organizer

        #get pitches from this comp

        #filter to ones not yet judged by me

        #filter to those with the lowest number of votes

        #choose one randomly

        #return
