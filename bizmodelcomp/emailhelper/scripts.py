from emailhelper.models import *
from judge.models import *
from competition.models import *
import csv

def init_echallenge(email_id=2):

    email = Bulk_email.objects.get(id=2)
    recipients = ""

    for sub in email.sub_val_set.all():
      sub.delete()

    reader = csv.reader(open('feedback.csv'), delimiter=',', quotechar='"')

    team = Sub_val(email=email, key="{team}")
    team.save()

    online_1 = Sub_val(email=email, key="{online comment 1}")
    online_1.save()
    online_2 = Sub_val(email=email, key="{online comment 2}")
    online_2.save()

    phase_1_quartile = Sub_val(email=email, key="{phase 1 quartile}")
    phase_1_quartile.save()
    phase_2_quartile = Sub_val(email=email, key="{phase 2 quartile}")
    phase_2_quartile.save()

    pitch_comment_1 = Sub_val(email=email, key="{pitch comment 1}")
    pitch_comment_1.save()
    pitch_comment_2 = Sub_val(email=email, key="{pitch comment 2}")
    pitch_comment_2.save()

    pitch_delta_1 = Sub_val(email=email, key="{pitch delta 1}")
    pitch_delta_1.save()
    pitch_delta_2 = Sub_val(email=email, key="{pitch delta 2}")
    pitch_delta_2.save()

    num = 0

    #for each line in csv..
    for row in reader:

        print 'rot len=%s: %s' % (len(row), row)

        founder_email = row[1]
        if (not founder_email) or len(founder_email) == 0:
            continue

        Val(sub_val=team, val=row[0], order=num).save() 

        online_comment_1 = "N/A"
        online_comment_2 = "N/A"
        #look up pitch for email
        try:

          pitch = Pitch.objects.get(owner__email=founder_email)
          print 'pitch: %s' % pitch

          judged = JudgedPitch.objects.filter(pitch=pitch)

          if len(judged) >= 1:
            online_comment_1 = judged[0].feedback
          if len(judged) >= 2:
            online_comment_2 = judged[1].feedback
        except:
          pitch = None

        print ''

        Val(sub_val=online_1, val=online_comment_1, order=num).save()
        Val(sub_val=online_2, val=online_comment_2, order=num).save()

        #set remaining vars from csv
        Val(sub_val=phase_1_quartile, val=row[3], order=num).save()
        Val(sub_val=phase_2_quartile, val=row[5], order=num).save()

        if len(row) > 7: Val(sub_val=pitch_comment_1, val=row[7], order=num).save()
        else: Val(sub_val=pitch_comment_1, val="N/A", order=num).save()

        if len(row) > 9: Val(sub_val=pitch_comment_2, val=row[9], order=num).save()
        else: Val(sub_val=pitch_comment_2, val="N/A", order=num).save()

        if len(row) > 8: Val(sub_val=pitch_delta_1, val=row[8], order=num).save()
        else: Val(sub_val=pitch_delta_1, val="N/A", order=num).save()
        
        if len(row) > 10: Val(sub_val=pitch_delta_2, val=row[10], order=num).save()
        else: Val(sub_val=pitch_delta_2, val="N/A", order=num).save()

        #if num % 5 == 0:
        #  founder_email = "robftz+%s@gmail.com" % founder_email.split('@')[0]
        #elif num %5 == 1:
        #  founder_email = "rob+%s@habitindustries.com" % founder_email.split('@')[0]
        #elif num %5 == 2:
        #  founder_email = "devin+%s@habitindustries.com" % founder_email.split('@')[0]
        #elif num % 5 == 3:
        #  founder_email = "devin+%s@ly.st" % founder_email.split('@')[0]
        #elif num % 5 == 4:
        #  founder_email = "devinhunt+%s@gmail.com" % founder_email.split('@')[0]

        if len(recipients) == 0:
            recipients = founder_email
        else:
            recipients = "%s;%s" % (recipients, founder_email)

        num += 1

    email.recipient_founders = recipients
    email.save()
