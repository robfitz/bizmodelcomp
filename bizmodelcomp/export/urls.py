from django.conf.urls.defaults import *

urlpatterns = patterns('',
    
    #list applicants (whole competition)
    (r'^(?P<phase_id>[0-9]{1,10})/scores.csv$',
         'export.views.scores_csv'),
)
