from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from emailhelper.models import Bulk_email
from competition.models import Competition



@login_required
def manage_email(request, comp_url):

    competition = get_object_or_404(Competition, hosted_url=comp_url)

    if competition.owner != request.user:
        return HttpResponseRedirect("/no_permissions/")

    email = Bulk_email.objects.filter(competition=competition)

    return render_to_response('emailhelper/dashboard.html', locals())



@login_required
def confirm_send_email(request, bulk_email_id):

    email = get_object_or_404(Bulk_email, id=bulk_email_id)

    if email.sent_on_date:
        return HttpResponseRedirect('/email/review/%s/' % bulk_email_id)

    return render_to_response('emailhelper/confirm_send_email.html', locals())



@login_required
def already_sent(request, bulk_email_id):

    email = get_object_or_404(Bulk_email, bulk_email_id)

    return render_to_response('emailhelper/summarize_sent_email.html', locals())

