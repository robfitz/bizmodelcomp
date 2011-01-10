from competition.models import *

try:
	import simplejson
except ImportError:
	import json as simplejson

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core import serializers

def set_phase_step(request, phase_id, comp_url=None,):

    print 'set phase step'

    obj = {"result": "failure"}

    phase = Phase.objects.get(id=phase_id)

    print 'phase: %s' % phase

    if request.user != phase.competition.owner:
        #no permissions
        print 'XXX no permissions!'
        return None

    try:
        setup_steps = PhaseSetupSteps.objects.get(phase=phase)
    except:
        setup_steps = PhaseSetupSteps(phase=phase)
        setup_steps.save()

    print 'setup steps %s' % setup_steps
    print 'method: %s' % request.method

    if request.method == "POST":

        print 'posting'

        #well that was easy
        try:
            form = PhaseSetupStepsForm(request.POST, instance=setup_steps)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            
        'print created form'
        form.save()
        print 'saved form'

        print '###########'
        print request.POST
        print '-----------'
        print form.as_p()
        print ''

        obj = {"result": "success"}
        
    json = simplejson.dumps(obj)
    
    return HttpResponse(json, mimetype="application/json")
