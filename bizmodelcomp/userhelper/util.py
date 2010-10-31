from random import Random
import string

from userhelper.models import VerificationKey
from emailhelper import send_email

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
            key = ''.join(Random().sample(string.letters+string.digits, 12))
            try:
                
                verification_key = VerificationKey(key=key,
                                                   user = user)
                verification_key.save()
                #if this hasn't thrown an exception, it's unique and we're
                #okay to quit searching
                break
            
            except: pass
            
        else:
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

    send_email(subject, message, to_email)

    return True
