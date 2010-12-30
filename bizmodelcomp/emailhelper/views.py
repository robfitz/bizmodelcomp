from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from emailhelper.models import Bulk_email, Email_address
from emailhelper.util import send_bulk_email
from emailhelper.forms import BulkEmailForm
from competition.models import Competition



@login_required
def manage_email(request, comp_url):

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    if competition.owner != request.user:
        return HttpResponseRedirect("/no_permissions/")

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

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    if competition.owner != request.user:
        return HttpResponseRedirect("/no_permissions/")

    email = get_object_or_404(Bulk_email, id=bulk_email_id)

    if request.method == "POST" and request.POST.get("confirm"):

        send_bulk_email(email)
        return HttpResponseRedirect("/dashboard/email/%s/" % comp_url)

    return render_to_response('emailhelper/review_email.html', locals())



@login_required
def already_sent(request, comp_url, bulk_email_id):

    competition = get_object_or_404(Competition, hosted_url=comp_url)
    if competition.owner != request.user:
        return HttpResponseRedirect("/no_permissions/")

    email = get_object_or_404(Bulk_email, id=bulk_email_id)

    return render_to_response('emailhelper/review_email.html', locals())

