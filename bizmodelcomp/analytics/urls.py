from django.conf.urls.defaults import *

urlpatterns = patterns('',

    #popups
    (r'^table/(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,100})/$',
        'analytics.views.table'),




)
