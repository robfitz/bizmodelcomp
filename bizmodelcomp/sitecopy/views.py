from sitecopy.models import SiteCopy
from django.shortcuts import get_object_or_404, render_to_response


def static_copy_popup(request, site_copy_id):

    title = site_copy_id

    copy = get_object_or_404(SiteCopy, id=site_copy_id).text

    return render_to_response('sitecopy/static_copy_popup.html', locals())



def static_copy(request, site_copy_id):

    title = site_copy_id

    copy = get_object_or_404(SiteCopy, id=site_copy_id).text

    return render_to_response('sitecopy/static_copy.html', locals())
