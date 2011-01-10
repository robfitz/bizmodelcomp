from django.conf.urls.defaults import *

urlpatterns = patterns('',
    
    #judge dashboard
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/$', 'judge.views.dashboard'),
                       
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/go/$', 'judge.views.judging'),

    (r'^go/(?P<unjudged_pitch_id>[0-9]{1,10})/$',
         'judge.views.judging'),

    (r'^review/(?P<judgedpitch_id>[0-9]{1,10})/$',
         'judge.views.judging'),

    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/list/$', 'judge.views.list'),

##    #list applicants (whole competition)
##    (r'^(?P<competition_id>[0-9]{1,10})/applicants/',
##         'dashboard.views.list_applicants'),
##
##    #list pitches (per phase)
##    (r'^(?P<competition_id>[0-9]{1,10})/phase/(?P<phase_id>[0-9]{1,10})/pitches/$',
##         'dashboard.views.list_pitches'),
##                       
##    #view details of a single submitted pitch
##    (r'^pitch/(?P<pitch_id>[0-9]{1,10})/$',
##         'dashboard.views.view_pitch'),
##                       
##
##    #list judges (per phase)
##    (r'^(?P<competition_id>[0-9]{1,10})/phase/(?P<phase_id>[0-9]{1,10})/judges/$',
##         'dashboard.views.list_judges'),
##
##    #delete judges (per phase)
##    (r'^(?P<competition_id>[0-9]{1,10})/phase/(?P<phase_id>[0-9]{1,10})/delete_judge_invites/$',
##         'dashboard.views.delete_judge_invites'),

)
