from bizmodelcomp.competition.models import *
from django.shortcuts import render_to_response
from django.template import loader, Context
from django.http import HttpResponse



#a debugging page checking how the javascript widget code displays
def form_test(request, competition_id):

    competition_id = 1
    return render_to_response('entercompetition/form_test.html', locals())



#a hosted microsite to accept contest applications
def applicationMicrosite(request, competition_id):

    #TODO: un-hardcode URL
    base_url = "http://localhost:8000"
    
    competition = Competition.objects.get(pk=competition_id)

    return render_to_response('entercompetition/application_microsite.html', locals())



#creates some slightly customized javascript to load the appropriate
#contest widget into the admin's page
def applicationWidget(request, competition_id):

    callback_function = "bmc_callback"

    form = """\
<form id="bmc_form" action="." method="GET" onsubmit="return apply(\\'%s\\')">\
    <p>\
    Name<br/>\
    <input type="text" name="name" id="bmc_field" />\
    </p>\
\
    <p>\
    Email<br/>\
    <input type="text" name="email" id="bmc_field" />\
    </p>\
\
    <p>\
    MM/DD/YYYY Birthday<br/>\
    <input type="text" name="month" id="bmc_field" size="2" max="2" />\
    <input type="text" name="day" id="bmc_field" size="2" max="2" />\
    <input type="text" name="year" id="bmc_field" size="4" max="4" />    \
    </p>\
\
    <input type="hidden" name="callback_function" id="bmc_field" value="%s"\
    <input type="submit" value="Register for competition" />\
</form>\
""" % (competition_id, callback_function)

    template = loader.get_template("entercompetition/widget.js")
    rendered = template.render(Context(locals()))

    return HttpResponse(rendered, mimetype="application/javascript")



#accepts a brand new application for the contest, which makes a
#Founder object to represent the applicant and hooks them into
#the contest to receive alerts and submit their full pitch
def applyToCompetition(request, competition_id):

    competition = Competition.objects.get(pk=competition_id)
    callback_function = "bmc_callback" #a probably correct default

    if competition and request.method == "GET" and len(request.GET) > 0:

        founder = Founder()
        
        for key in request.GET:
            
            print "%s: %s" % (key, request.GET[key])

            #set standard/required values
            if key in dir(founder):
                setattr(founder, key, request.GET[key])

        try: callback_function = request.GET["callback_function"]
        except: pass

        founder.save()
        competition.applicants.add(founder)
        message = "Sweet, you in the competition!"

    else:
        message = "Sorry, the application service is temporarily down. Please try again soon."

    params = '{ "message": "%s"}' % message
    response = "%s( %s )" % (callback_function, params)

    return HttpResponse(response, mimetype="application/javascript")


