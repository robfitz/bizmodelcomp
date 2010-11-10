from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'competition.views.index'),

    #setup a contest
    (r'^new_competition/$', 'competition.views.edit_competition'),

    (r'^edit_competition/(?P<competition_id>[0-9]{1,10})/$',
         'competition.views.edit_competition'),

    (r'^edit_application/(?P<phase_id>[0-9]{1,10})/$',
         'competition.views.edit_application'),

    (r'^edit_phases/(?P<competition_id>[0-9]{1,10})/$',
         'competition.views.edit_phases'),

    (r'^edit_application_widgets/(?P<competition_id>[0-9]{1,10})/$',
         'competition.views.edit_application_widgets'),

)
