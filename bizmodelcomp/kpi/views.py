from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

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


def get_ative_students():

    active_competitions = []

    for comp in Competition.objects.all():
        if len(comp.phases()) > 0: 
            last_phase = comp.phases()[-1]

    return 0


def get_active_students():

    return 0 


def get_paid_competitions():

    return 0


def get_marketing_subscribers():

    return 0
