from utils.util import rand_key

from userhelper.models import VerificationKey
from emailhelper.util import send_email

def send_verification_email(user, next_page):

    verification_key = None

    try:
        #only one per user. if we've already made one, send
        #a friendly reminder
        verification_key = VerificationKey.objects.get(user=user)
    except:

        #create unique random verification key. it's possible these loops
        #won't find one, but that's quite unlikely and 500ing seems less
        #risky potentially infinite looping
        for attempt in range(1, 1000):
            key = rand_key()
            print 'send veri email: key %s' % key
            try:
                
                verification_key = VerificationKey(key=key,
                                                   user = user)
                print 'made veri key'
                verification_key.save()
                print 'saved veri key'
                #if this hasn't thrown an exception, it's unique and we're
                #okay to quit searching
                print 'breakin'
                break
            
            except: pass
            
        else:
            print 'couldnt find unique valid key, aborting'
            #couldn't create a unique valid key for some reason
            return False

    verification_path = "/accounts/verify/%s/?next=%s" % (verification_key.key, next_page)
    verification_link = request.build_absolute_uri(verification_path)

    subject = "Verify your competition account"
    to_email = user.email
    message = """Hello,

To keep the competition pitches secure, we need you to confirm that this really is your email address, which you can do by using the link below. You'll then be taken to the page you were heading toward when you registered.

%s

Thanks very much, and please let us know (you can just reply to this email) if you have any questions or issues.

Stay well,
nvana""" % (verification_link)

    print 'sending email verify email'
    send_email(subject, message, to_email)

    return True



#this function harmlessly accepts a False or invalid parameter, so
#views may simply call it as:
#got_ev_key(request.GET.get("ev", False))
#
#TODO: automate the check for the &ev param as soon as any request is made
def got_ev_key(email_verification_key):
    if email_verification_key:

        try:
            #since someone clicked on the link, which was more-or-less
            #unguessable, we can assume that the email it was registered
            #to is valid and don't need to test it again when that person registers
            key = VerificationKey.objects.get(key=email_confirmed)
            key.is_verified = True
            key.save()

        except:
            #no harm if it was bogus
            pass
