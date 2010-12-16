from django.conf.urls.defaults import *

urlpatterns = patterns('',

    #setup new competition
    (r'^setup/(?P<step_num>[0-9]{1,2})/$',
        'dashboard.views.setup'),

    #email applicants that phase is opening. applies only to competition's current phase
    (r'^announce_applications_open/$', 'dashboard.views.announce_applications_open'),

    #email judges that judging is open and set it to open
    (r'^announce_judging_open/$', 'dashboard.views.announce_judging_open'),

    #email contestants their feedback from phases 2 & 3
    (r'^send_competition_feedback/$', 'dashboard.views.send_competition_feedback'),

    #edit basic details of existing comp
    (r'edit_comp_details/$', 'dashboard.views.edit_comp_details'),

    #ajaxy stuff
    (r'^ajax/phase_steps/(?P<phase_id>[0-9]{1,10})/$',
         'dashboard.ajax.set_phase_step'),
         
    #organizer dashboard - overview
    (r'^$', 'dashboard.views.dashboard'),

    #org dashboard - individual phase
    (r'^phase/(?P<phase_id>[0-9]{1,10})/$',
         'dashboard.views.dashboard'),

    #set a particular phase to active
    (r'^phase/(?P<phase_id>[0-9]{1,10})/set_current/$',
         'dashboard.views.set_current_phase'),

    #org dash - edit phases
    (r'^(?P<competition_id>[0-9]{1,10})/phases/$',
         'dashboard.views.edit_phases'),

    #list applicants (whole competition)
    (r'^(?P<competition_id>[0-9]{1,10})/applicants/$',
         'dashboard.views.list_applicants'),

    #edit application (per phase)
    (r'^phase/(?P<phase_id>[0-9]{1,10})/application/$',
         'dashboard.views.edit_application'),

    #list pitches (per phase)
    (r'^(?P<competition_id>[0-9]{1,10})/phase/(?P<phase_id>[0-9]{1,10})/pitches/$',
         'dashboard.views.list_pitches'),
    
    #view details of a single submitted pitch
    (r'^pitch/(?P<pitch_id>[0-9]{1,10})/$',
         'dashboard.views.view_pitch'),
                       
    #view details of a pitch judgement
    (r'^judgement/(?P<judgement_id>[0-9]{1,10})/$',
         'dashboard.views.view_judgement'),

    #view details of the judgements a judge has made
    (r'^(?P<competition_id>[0-9]{1,10})/phase/(?P<phase_id>[0-9]{1,10})/judgements/(?P<judge_id>[0-9]{1,10})/$',
         'dashboard.views.list_judgements'),

    #list judges (per phase)
    (r'^(?P<competition_id>[0-9]{1,10})/phase/(?P<phase_id>[0-9]{1,10})/judges/$',
         'dashboard.views.list_judges'),

    #delete judges (per phase)
    (r'^(?P<competition_id>[0-9]{1,10})/phase/(?P<phase_id>[0-9]{1,10})/delete_judge_invites/$',
         'dashboard.views.delete_judge_invites'),

)
