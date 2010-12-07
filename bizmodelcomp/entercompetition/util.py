from emailhelper.util import send_email
from competition.models import Competition, Pitch

def send_deadline_reminder_to_entrant(pitch):

    competition = pitch.phase.competition

    edit_pitch_link = "http://londonentrepreneurschallenge.nvana.com/apply/pitch/echallenge/?f=%s" % pitch.owner.anon_key().key

    to_email = pitch.owner.email.split(',')[0]
    subject = "6 hours left to edit your application"
    message = """Hello,

Thanks for applying to %s.

The deadline for Phase One submissions is 11:59pm tonight, October 31.

Remember that there are prizes of 2000 pounds for this phase of the competition, plus more to come later. You can keep editing and refining your pitch up until the deadline using this link:

%s

If you run into any problems or have questions about the application process, please feel free to respond to this email. 

Sincerely,

The %s team""" % (competition.name, edit_pitch_link, competition.name)

    send_email(subject, message, to_email)
