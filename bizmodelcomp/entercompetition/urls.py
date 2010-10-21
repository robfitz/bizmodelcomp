from django.conf.urls.defaults import *

urlpatterns = patterns('',

    #partially customized javascript that you can embed on a site
    #to accept contest registrations
    (r'^(?P<competition_url>[-_a-zA-Z0-9]{1,10})/widget.js$',
         'entercompetition.views.applicationWidget'),

    #ajax call from the widget which creates an entry & returns a message
    (r'^(?P<competition_url>[-_a-zA-Z0-9]{1,10})/$',
         'entercompetition.views.applyToCompetition'),    

    #the application widget sitting on a standalone site
    (r'^(?P<competition_url>[-_a-zA-Z0-9]{1,10}).html$',
         'entercompetition.views.applicationMicrosite'),

    #form where you upload files & file in answers
    (r'^pitch/(?P<competition_url>[-_a-zA-Z0-9]{1,10})/$',
         'entercompetition.views.edit_pitch'),

    #redirect from form after saving a pitch
    (r'^pitch_saved/(?P<competition_url>[-_a-zA-Z0-9]{1,10})/$',
         'entercompetition.views.submit_pitch'),
                       
)
