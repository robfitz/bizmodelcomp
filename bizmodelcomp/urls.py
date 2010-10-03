from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    #local assets                  
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': 'C:/www/bizmodelcomp/media'}),
    
    #admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    #biz model competition
    (r'^', include('bizmodelcomp.competition.urls')),

    #login, register, etc
    (r'^accounts/', include('bizmodelcomp.userhelper.urls')),

    #apply to comp
    (r'^apply/', include('bizmodelcomp.entercompetition.urls')),
)
