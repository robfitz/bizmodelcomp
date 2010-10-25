from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

import bizmodelcomp.competition
import bizmodelcomp.competition.views

import entercompetition.views

urlpatterns = patterns('',

    #local assets                  
    (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': '../media'}),
    
    #admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    #biz model competition
    (r'^', include('bizmodelcomp.competition.urls')),

    #login, register, etc
    (r'^accounts/', include('bizmodelcomp.userhelper.urls')),

    #apply to comp
    (r'^apply/', include('bizmodelcomp.entercompetition.urls')),

    #specific campaign clobbers
    (r'^echallenge/',
         'entercompetition.views.edit_pitch',
         {'competition_url': 'echallenge'}), 
)
