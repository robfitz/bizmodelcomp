from django.conf.urls.defaults import *

urlpatterns = patterns('',

    #edit application (per phase)
    (r'^phase/(?P<phase_id>[0-9]{1,100})/application/$',
         'dashboard.views.edit_application'),

    #advance to next phase
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/next_phase/$', 'dashboard.views.next_phase'),

    #organizer dashboard - overview
    (r'^$', 'dashboard.views.overall_dashboard'),

    #setup new competition
    (r'^new_comp/$',
        'dashboard.views.setup'),
    (r'^(?P<comp_id>[0-9]{1,100})/setup/(?P<step_num>[0-9]{1,2})/$',
        'dashboard.views.setup'),

    #organizer dashboard - setup & comp info
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/setup/$', 'dashboard.views.edit_comp'),
    
    #organizer dashboard - manage current phase
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/$', 'dashboard.views.dashboard'),
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/manage/$', 'dashboard.views.dashboard'),


    #pass off email to someone more qualified
    (r'^email/', include('bizmodelcomp.emailhelper.urls')), 

    #data slicing & dicing, spreadsheets, etc
    (r'data/', include('bizmodelcomp.analytics.urls')),

    #email applicants that phase is opening. applies only to competition's current phase
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/announce_applications_open/$', 'dashboard.views.announce_applications_open'),
    #email judges that judging is open and set it to open
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/announce_judging_open/$', 'dashboard.views.announce_judging_open'),
    #email contestants their feedback from phases 2 & 3
    (r'^send_competition_feedback/$', 'dashboard.views.send_competition_feedback'),

    #edit basic details of existing comp
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/edit_comp/$', 'dashboard.views.edit_comp'),

    #ajaxy stuff
    (r'^ajax/phase_steps/(?P<phase_id>[0-9]{1,100})/$',
         'dashboard.ajax.set_phase_step'),
         
    #org dashboard - individual phase
    (r'^phase/(?P<phase_id>[0-9]{1,100})/$',
         'dashboard.views.dashboard'),

    #set a particular phase to active
    (r'^phase/(?P<phase_id>[0-9]{1,100})/set_current/$',
         'dashboard.views.set_current_phase'),

    #list applicants (whole competition)
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/applicants/$',
         'dashboard.views.list_applicants'),


    #list pitches (per phase)
    (r'^phase/(?P<phase_id>[0-9]{1,100})/pitches/$',
         'dashboard.views.list_pitches'),
    
    #view details of a single submitted pitch
    (r'^pitch/(?P<pitch_id>[0-9]{1,100})/$',
         'dashboard.views.view_pitch'),
                       
    #view details of a pitch judgement
    (r'^judgement/(?P<judgement_id>[0-9]{1,100})/$',
         'dashboard.views.view_judgement'),

    #view details of the judgements a judge has made
    (r'^phase/(?P<phase_id>[0-9]{1,100})/judgements/(?P<judge_id>[0-9]{1,100})/$',
         'dashboard.views.list_judgements'),

    #list judges (per phase)
    (r'^phase/(?P<phase_id>[0-9]{1,100})/judges/$',
         'dashboard.views.list_judges'),

    #delete judges (per phase)
    (r'^delete_judge_invites/$',
         'dashboard.views.delete_judge_invites'),

)
