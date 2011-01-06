from django.conf.urls.defaults import *

urlpatterns = patterns('',

    (r'^$', 'new_comp.views.new'),

    (r'^who/$', 'new_comp.views.who'),

    (r'^phases/$', 'new_comp.views.phase_structure'),

    (r'^details/$', 'new_comp.views.competition_details'),

)
