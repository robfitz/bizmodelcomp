from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       
    (r'^(?P<competition_id>[0-9]{1,10})/widget.js$',
         'entercompetition.views.applicationWidget'),
    (r'^(?P<competition_id>[0-9]{1,10})/test$',
         'entercompetition.views.form_test'),
    (r'^(?P<competition_id>[0-9]{1,10})/$',
         'entercompetition.views.applyToCompetition'),    
    
    (r'^(?P<competition_id>[0-9]{1,10}).html$',
         'entercompetition.views.applicationMicrosite'),

    (r'^pitch/(?P<competition_id>[0-9]{1,10})/$',
         'entercompetition.views.edit_pitch'),
                       
)
