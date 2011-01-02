from django.conf.urls.defaults import *

urlpatterns = patterns('',

    #landing page
    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,10})/$',
        'analytics.views.dashboard'),



)
