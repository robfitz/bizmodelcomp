from settings import is_local, EMAIL_USER, EMAIL_PASSWORD, EMAIL_DEFAULT_FROM, DISABLE_ALL_EMAIL, EMAIL_LOG
import markdown
from datetime import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, message_markdown, to_email, from_email=EMAIL_DEFAULT_FROM):

    print('sent email!')

    log_folder = '/'.join(EMAIL_LOG.split('/')[0:-1])
    print 'email folder: %s' % log_folder
    if not os.path.isdir(log_folder):
        os.mkdir(log_folder)

    #log it
    f = open(EMAIL_LOG, 'a')
    f.write("------------------------\n")
    f.write("SUBJECT:  %s\n" % subject)
    f.write("TO:       %s\n" % to_email)
    f.write("FROM:     %s\n" % from_email)
    f.write("DATE:     %s\n" % datetime.now())
    f.write("BODY:   \n%s\n\n\n" % message_markdown)
    f.close()
    
    #don't send emails in debug mode, which covers both local
    #and testing stuff on the liver servers
    if is_local or DISABLE_ALL_EMAIL:
        return 

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
     
    # Create the body of the message (a plain-text and an HTML version).
    text = message_markdown
    html = markdown.markdown(message_markdown)
     
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
    result = s.login(username, password)

    print 'send mail %s %s %s' % (from_email, to_email, msg.as_string())
     
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    result = s.sendmail(from_email, to_email, msg.as_string())
    s.quit()
