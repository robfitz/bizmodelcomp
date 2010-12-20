from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login/$', 'userhelper.views.loginRegister'),
    (r'^logout/$', 'userhelper.views.logoutUser'),
    (r'^register/$', 'userhelper.views.loginRegister'),
    (r'^no_permissions/$', 'userhelper.views.noPermissions'),
    (r'^verify_email/$', 'userhelper.views.verify_email'),
)
