import sys
try:
	import simplejson
except ImportError:
	import json as simplejson

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from emailhelper.models import *
from emailhelper.util import send_bulk_email
from emailhelper.forms import BulkEmailForm
from competition.models import Competition
from sitecopy.models import SiteCopy
from utils.util import rand_key






def newsletter_subscribe(request):

    print 'newsletter subscript'

    email = request.POST.get("email")
    default_alert = "We ran into some unexpected difficulties signing you up. Please try again with another email address or at another time."
    result = "failure"
    alert = None

    print 'got email: %s' % email

    if NewsletterSubscription.objects.filter(email=email).count() == 0:
        print "doesn't already exist"
        #add subscriber if it's a new one

        if email.find('@') != -1 and email.find('.') != -1:
            print 'looks valid!'

            for i in range(1,10):
                try:
                    subscription = NewsletterSubscription(email=email)
                    subscription.unsubscribe_key = rand_key(length=10)
                    print 'rand? %s' % subscription.unsubscribe_key
                    subscription.save()
                    alert = "Thanks so much for joining the newsletter. We'll keep you in the loop about noteworthy developments."
                    result = "success"
                    break
                except:
                    print sys.exc_info()[0]
                    pass
        else:
            print 'invalid :('
            #doesn't look like a legit email address
            alert = "That doesn't look like an email address, so we weren't able to put you on the list. Please try again?"

    else:
        print 'already got emial'
        alert = "That email is already on the list, so you should receive the newsletters as we send them. Maybe check your spam box if they're not arriving?"

    if not alert:
        alert = default_alert

        failed_subscription = FailedNewsletterSubscription(email=email)
        failed_subscription.save()

    print 'returning result: %s' % alert
    obj = { "result": result, "alert": alert }
    json = simplejson.dumps(obj)


    return HttpResponse(json, mimetype="application/json")

    

def newsletter_unsubscribe(request, unsubscribe_key):

    alert_title = "All done:"
    alert = None
    try:
        subscription = NewsletterSubscription.objects.get(unsubscribe_key=unsubscribe_key)

        unsubscription = NewsletterUnsubscription(subscription_timestamp=subscription.timestamp, email=subscription.email)
        unsubscription.save() 

        alert = "Your email, %s, has been removed from our mailing list. Thanks for giving us a try, and please <a href='/contact/'>let us know</a> if there's anything we can do to help out." % subscription.email

        subscription.delete()

    except:
        alert_title = "Quick question:"
        alert = "It looks like the requested email has been already removed from our mailing list at some previous point.  Are you still getting messages? If so, please <a href='/contact/'>contact us</a> and we'll sort it out as quickly as we can."

    return render_to_response('emailhelper/unsubscribe.html', locals())



@login_required
def manage_email(request, comp_url):

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    if competition.owner != request.user:
        return HttpResponseRedirect("/no_permissions/")

    intro = ""
    try:
        intro = SiteCopy.objects.get(id="intro_dashboard_email")
    except:
        pass

    #a blank new message, to edit and save as a draft
    new_email_form = BulkEmailForm(instance = Bulk_email(competition=competition))

    if request.method == "POST":
        
        if request.POST.get("form_name") == "new_draft":
            #saving new email draft
            saved_form = BulkEmailForm(request.POST)              
            new_email=saved_form.save(commit=False)
            new_email.competition = competition
            new_email.phase = competition.current_phase #seems like a safe default
            new_email.save()

            #recipients
            if request.POST.get("recipient_type") == "applicants":
                
                for i, founder in enumerate(competition.current_phase.applicants()):

                    if founder is not None:

                        recipient = Email_address(order=i, 
                                bulk_email=new_email,
                                address=founder.email,
                                user=founder.user)
                        recipient.save()

            elif request.POST.get("recipient_type") == "submitted_pitches":

                for i, pitch in enumerate(competition.current_phase.pitches(num=0)):

                    if pitch is not None and pitch.team is not None:

                        recipient = Email_address(order=i, 
                                bulk_email=new_email,
                                address=pitch.team.owner.email,
                                user=pitch.team.owner.user)
                        recipient.save()

            elif request.POST.get("recipient_type") == "judges":

                for i, judge in enumerate(competition.current_phase.judges()):

                    recipient = Email_address(order=i, 
                            bulk_email=new_email,
                            address=judge.email,
                            user=judge.user)
                    recipient.save()


    #all my existing mail, to list
    emails = Bulk_email.objects.filter(competition=competition)

    return render_to_response('emailhelper/dashboard.html', locals())



@login_required
def confirm_send_email(request, comp_url, bulk_email_id):

    intro = ""
    try:
        intro = SiteCopy.objects.get(id="intro_dashboard_email")
    except:
        pass

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    if competition.owner != request.user:
        return HttpResponseRedirect("/no_permissions/")

    email = get_object_or_404(Bulk_email, id=bulk_email_id)

    if request.method == "POST" and request.POST.get("confirm"):

        send_bulk_email(email)
        return HttpResponseRedirect("/dashboard/email/%s/" % comp_url)

    return render_to_response('emailhelper/review_email.html', locals())



@login_required
def review_email_popup(request, bulk_email_id):

    intro = ""
    try:
        intro = SiteCopy.objects.get(id="intro_dashboard_email")
    except:
        pass

    email = get_object_or_404(Bulk_email, id=bulk_email_id)

    competition = email.competition
    if competition.owner != request.user:
        return HttpResponseRedirect("/no_permissions/")

    return render_to_response("emailhelper/review_email_popup.html", locals())



@login_required
def already_sent(request, comp_url, bulk_email_id):

    intro = ""
    try:
        intro = SiteCopy.objects.get(id="intro_dashboard_email")
    except:
        pass

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    if competition.owner != request.user:
        return HttpResponseRedirect("/no_permissions/")

    email = get_object_or_404(Bulk_email, id=bulk_email_id)

    return render_to_response('emailhelper/review_email.html', locals())

