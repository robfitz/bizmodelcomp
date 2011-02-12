from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from kpi.models import *

@login_required
def index(request):

    if not request.user.is_staff:
        return HttpResponseRedirect('/dashboard/')

    paid_competitions = get_paid_competitions() 
    active_students = get_active_students()
    marketing_subscribers = get_marketing_subscribers()

    return render_to_response("kpi/index.html", locals())


def get_paid_competitions():

    return 0


def get_active_students():

    snapshots = ActiveStudents.objects.all()
    print 'got snapshots: %s' % snapshots
    latest_snapshot = snapshots[0]
    print 'latest: %s' % latest_snapshot
    return latest_snapshot.total



def get_marketing_subscribers():

    return 0
