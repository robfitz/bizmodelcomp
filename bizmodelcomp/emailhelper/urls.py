from django.conf.urls.defaults import *

urlpatterns = patterns('',

    (r'^confirm/(?P<bulk_email_id>[0-9]{1,10})/$', 'emailhelper.views.confirm_send_email'),

    (r'^review/(?P<bulk_email_id>[0-9]{1,10})/$', 'emailhelper.views.already_sent'),

)

    
