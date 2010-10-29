from django.conf.urls.defaults import *

urlpatterns = patterns('',
    
    #organizer dashboard
    (r'^$', 'dashboard.views.dashboard'),

    #list applicants (whole competition)
    (r'^(?P<competition_id>[0-9]{1,10})/applicants/',
         'dashboard.views.list_applicants'),

    #list pitches (per phase)
    (r'^(?P<competition_id>[0-9]{1,10})/phase/(?P<phase_id>[0-9]{1,10})/pitches/$',
         'dashboard.views.list_pitches'),
                       
    #view details of a single submitted pitch
    (r'^pitch/(?P<pitch_id>[0-9]{1,10})/$',
         'dashboard.views.view_pitch'),
                       

    #list judges (per phase)
    (r'^(?P<competition_id>[0-9]{1,10})/phase/(?P<phase_id>[0-9]{1,10})/judges/$',
         'dashboard.views.list_judges'),

    #list judges (per phase)
    (r'^(?P<competition_id>[0-9]{1,10})/phase/(?P<phase_id>[0-9]{1,10})/invite_judges/$',
         'dashboard.views.invite_judges'),

)
