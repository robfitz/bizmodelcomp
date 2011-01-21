from django.conf.urls.defaults import *

urlpatterns = patterns('',

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
