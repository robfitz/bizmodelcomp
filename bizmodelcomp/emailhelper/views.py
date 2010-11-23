from emailhelper.models import Bulk_email

from django.shortcuts import render_to_response, get_object_or_404



def confirm_send_email(request, bulk_email_id):

    email = get_object_or_404(Bulk_email, id=bulk_email_id)

    if email.sent_on_date:
        return HttpResponseRedirect('/email/review/%s/' % bulk_email_id)

    return render_to_response('emailhelper/confirm_send_email.html', locals())



def already_sent(request, bulk_email_id):

    email = get_object_or_404(Bulk_email, bulk_email_id)

    return render_to_response('emailhelper/summarize_sent_email.html', locals())

