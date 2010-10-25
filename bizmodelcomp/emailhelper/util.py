from settings import DEBUG, EMAIL_USER, EMAIL_PASSWORD, EMAIL_DEFAULT_FROM
import markdown

def send_email(from_email, to_email, subject, message_markdown):
    
    #don't send emails in debug mode, which covers both local
    #and testing stuff on the liver servers
    if DEBUG:
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
