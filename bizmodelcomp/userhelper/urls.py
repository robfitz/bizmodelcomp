from django.conf.urls.defaults import *

urlpatterns = patterns('',

    (r'^login/$', 'userhelper.views.loginRegister'),
    (r'^logout/$', 'userhelper.views.logoutUser'),
    (r'^register/$', 'userhelper.views.loginRegister'),
    (r'^no_permissions/$', 'userhelper.views.noPermissions'),
    (r'^verify_email/$', 'userhelper.views.verify_email'),
    (r'^settings/$', 'userhelper.views.account_settings'),

    (r'^pw_reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'userhelper/password_reset.html'}),
    (r'^pw_reset/done/$', 'django.contrib.auth.views.password_reset_done'),

    (r'^pw_change/$', 'django.contrib.auth.views.password_change', 
        {'template_name': 'userhelper/password_change.html'}),
    (r'^pw_change/done/$', 'django.contrib.auth.views.password_change_done'),
    


)
