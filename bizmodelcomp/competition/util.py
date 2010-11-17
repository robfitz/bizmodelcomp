from competition.models import *
from settings import is_local
from datetime import datetime
from judge.models import *


def get_competition_for_user(user):

    #are they an organizer?
    owned = Competition.objects.filter(owner = user)
    if owned.count() > 0:
        #TODO: handle multiple comps
        return owned[0]

    #are they a judge?
    judging = JudgeInvite.objects.filter(user = user)
    if judging.count() > 0:
        return judging[0]

    #nope
    return None


def sync_echallenge():

    if not is_local:
        csv_url = "lec.csv"
        competition = Competition.objects.get(hosted_url='echallenge')
    else:
        #debugging
        csv_url = "C:/Users/robfitz/Downloads/lec.csv"
        competition = Competition.objects.get(hosted_url='echallenge')

    f = open(csv_url)
    
    for line in f.readlines():

        chunks = line.split(',')
        try:
            email = chunks[3].strip("'")
            email = email.strip()
        except:
            pass

        try: name = unicode(chunks[1].strip("'")) + " " + unicode(chunks[2].strip("'"))
        except: name = ""

        try: birth = chunks[8].strip("'")
        except: birth = ""

        try: phone = chunks[4].strip("'")
        except: phone = ""

        if email and len(email) > 0:
            
            if Founder.objects.filter(email=email).count() > 0:
                #we recognize this email....
                founder = Founder.objects.get(email=email)

                if founder in competition.applicants.all():
                    #we already know this person. ignore as old duplicate
                    pass
                else:
                    #we know about them from previous contests, so just
                    #register the existing user to this one
                    competition.applicants.add(founder)
                    print 'associated existing founder w/ ECHALLENGE %s' % email
                
                print 'already have founder %s' % email
            else:
                print 'creating new founder for %s' % email
                #a new person we don't yet know. make an entry for them.
                #Note that this is the only time require_authentication is
                #set to false, since there's not a clean way to guarantee
                #they are who they claim to be before using our system at
                #least once, and the downside of getting it wrong is minimal
                #since the real person will get an email alert and be able
                #update/fix/delete the entries.
                founder = Founder(name = name,
                                  email = email,
                                  phone = phone,
                                  birth = birth,
                                  require_authentication=False)
                founder.save()

                #connect to competition we loaded data from
                competition.applicants.add(founder)
                competition.save()

    f.close()                
                              
