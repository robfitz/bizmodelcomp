from django.conf.urls.defaults import *

urlpatterns = patterns('',


    #/apply/sc2010/widget.js
    #partially customized javascript that you can embed on a site
    #to accept contest registrations
    (r'^(?P<competition_url>[-_a-zA-Z0-9]{1,50})/widget.js$',
         'entercompetition.views.applicationWidget'),

    #/apply/enter_competition/sc2010/
    #ajax call from the widget which creates an entry & returns a message
    (r'^enter_competition/(?P<competition_url>[-_a-zA-Z0-9]{1,50})/$',
         'entercompetition.views.applyToCompetition'),    

    #/apply/sc2010.html
    #a hosted entry form for collecting applicant personal details
    (r'^(?P<competition_url>[-_a-zA-Z0-9]{1,50}).html$',
         'entercompetition.views.applicationMicrosite'),

    #/apply/pitch/sc2010
    #form where applicant uploads files & fills in answers
    (r'^pitch/(?P<competition_url>[-_a-zA-Z0-9]{1,50})/$',
         'entercompetition.views.edit_pitch'),

    #/apply/load/
    #show info about getting back to an old version of an application,
    #and allow them to send an email reminder w/ the unique link
    (r'^load/(?P<competition_url>[-_a-zA-Z0-9]{1,50})/$',
         'entercompetition.views.recover_application'),

    #/apply/sent_reminder/
    #tell them that a login reminder has been emailed to them
    (r'^sent_reminder/$',
         'entercompetition.views.sent_reminder'),

    (r'^(?P<comp_url>[-_a-zA-Z0-9]{1,50})/$', 'entercompetition.views.submit_team'),
    (r'^(?P<comp_url>[-_a-zA-Z0-9]{1,50})/pitch/$', 'entercompetition.views.submit_business'),
)
