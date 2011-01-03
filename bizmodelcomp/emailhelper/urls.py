from django.conf.urls.defaults import *

urlpatterns = patterns('',

    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,10})/confirm/(?P<bulk_email_id>[0-9]{1,10})/$', 'emailhelper.views.confirm_send_email'),

    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,10})/archive/(?P<bulk_email_id>[0-9]{1,10})/$', 'emailhelper.views.already_sent'),

    (r'^(?P<comp_url>[-_:!()@#$%* a-zA-z0-9]{1,10})/$', 'emailhelper.views.manage_email'),

    (r'^unsubscribe/(?P<unsubscribe_key>[a-zA-Z0-9]{1,10})/$', 'emailhelper.views.newsletter_unsubscribe'),

)

    
