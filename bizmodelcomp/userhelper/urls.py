from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login/$', 'userhelper.views.loginUser'),
    (r'^logout/$', 'userhelper.views.logoutUser'),
    (r'^register/$', 'userhelper.views.registerUser'),
    (r'^no_permissions/$', 'userhelper.views.noPermissions'),
    (r'^verify_email/$', 'userhelper.views.verify_email'),
)
