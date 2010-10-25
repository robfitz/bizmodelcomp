from competition.models import Founder
from settings import is_local
from datetime import datetime

def sync_echallenge():

    if not is_local:
        csv_url = "http://www.londonentrepreneurschallenge.com/lec.csv"
    else:
        #debugging
        csv_url = "C:/Users/robfitz/Downloads/lec.csv"

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
                #we already know this person! ignore as old entry
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
                              
