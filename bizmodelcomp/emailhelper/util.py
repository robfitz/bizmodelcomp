from settings import is_local, EMAIL_USER, EMAIL_PASSWORD, EMAIL_DEFAULT_FROM, DISABLE_ALL_EMAIL, EMAIL_LOG
import markdown
from datetime import datetime
import os
import time

#sendgrid stuff
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#send a bunch of emails. message_markdown should have substitution strings already embedded
#in it.
#
#recipients is a list [email1, email2, email3]
#substitutions is dict of lists { '-name-': ['rob', 'tom', 'joe'],
#                                 '-team-': ['the cats', 'the dogs', 'the bogs'] }
def send_bulk_email(bulk_email, fromEmail=None, log=True):

    toEmail = "irrelevant@example.com"

    hdr = SmtpApiHeader.SmtpApiHeader()

    hdr.addTo(bulk_email.recipients())
              
    for sub, val in bulk_email.substitutions().items():
        hdr.addSubVal(sub, val)

    #TODO: probably not accurate!
    hdr.setCategory("initial")

    #hdr.addFilterSetting("footer", "enable", 1)

    msg = MIMEMultipart('alternative')
    msg['Subject']  = bulk_email.subject
    msg['From']     = fromEmail
    msg['To']       = toEmail
    msg["X-SMTPAPI"] = hdr.asJSON()

    text = bulk_email.message_markdown
    html = markdown.markdown(bulk_email.message_markdown)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
     
    # Attach parts into message container.
    msg.attach(part1)
    msg.attach(part2)

    # Login credentials
    username = EMAIL_USER
    password = EMAIL_PASSWORD

    # Open a connection to the SendGrid mail server
    s = smtplib.SMTP('smtp.sendgrid.net')
     
    # Authenticate
    s.login(username, password)
     
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(fromEmail, toEmail, msg.as_string())
     
    s.quit()


def send_email(subject, message_markdown, to_email, from_email=None, log=True):

    if not from_email: from_email = EMAIL_DEFAULT_FROM

    print('sent email!')

    log_folder = '/'.join(EMAIL_LOG.split('/')[0:-1])
    print 'email folder: %s' % log_folder
    if not os.path.isdir(log_folder):
        os.mkdir(log_folder)

    #log it
    f = open(EMAIL_LOG, 'a')
    if log: f.write("------------------------\n")
    if log: f.write("SUBJECT:  %s\n" % subject)
    if log: f.write("TO:       %s\n" % to_email)
    if log: f.write("FROM:     %s\n" % from_email)
    if log: f.write("DATE:     %s\n" % datetime.now())
    if log: f.write("BODY:   \n%s\n\n" % message_markdown)
    #f.close()
    
    #don't send emails in debug mode, which covers both local
    #and testing stuff on the liver servers
    if is_local or DISABLE_ALL_EMAIL:
        if log: f.write("DEBUG: aborting email because is_local=%s or DISABLE_ALL_EMAIL=%s\n" % (is_local, DISABLE_ALL_EMAIL))
        return 

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    if log: f.write("DEBUG: created MIMEMultipart\n")

    # Create the body of the message (a plain-text and an HTML version).
    text = message_markdown
    html = markdown.markdown(message_markdown)
    
    if log: f.write("       created message markdown\n")
 
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    if log: f.write("       created MIMEText\n")
 
    # Attach parts into message container.
    msg.attach(part1)
    msg.attach(part2)
     
    # Login credentials
    username = EMAIL_USER
    password = EMAIL_PASSWORD

    close_smtp = False
    if not smtp: 
        # Open a connection to the SendGrid mail server
        smtp = smtplib.SMTP('smtp.sendgrid.net')
        close_smtp = True
        

    if log: f.write("       created SMTP connection to sendgrid\n")

    # Authenticate
    result = smtp.login(username, password)

    if log: f.write("       logged in with result=%s\n" % str(result))

    print 'send mail %s %s %s' % (from_email, to_email, msg.as_string())
     
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    result = smtp.sendmail(from_email, to_email, msg.as_string())
    
##    debug_address = 'robftz+nvanadebug@gmail.com'
##    if close_smtp:
##        send_email(subject, message_markdown, debug_address, from_email, False)
##    else:
##        send_email(subject, message_markdown, debug_address, from_email, False, smtp)

    #send a copy of every email to rob for debugging
    #result_debug = s.sendmail(from_email, "robftz+nvanadebug@gmail.com", msmg.as_string())

    if log: f.write("       sent mail with result=%s\n\n\n" % str(result))

    if close_smtp:
        smtp.quit()

    #send a duplicate of the email to rob for debugging

##    if to_email != debug_address:
##        time.sleep(5)
##
##        send_email(subject, message_markdown, debug_address, from_email, False)
