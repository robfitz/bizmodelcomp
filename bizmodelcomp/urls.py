from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

import bizmodelcomp.competition
import bizmodelcomp.competition.views

import entercompetition.views

urlpatterns = patterns('',

    #temporary 
    #(r'^$',
    #    'entercompetition.views.edit_pitch',
    #    {'competition_url': 'echallenge'}), 

    #local assets                  
    (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': '../media'}),
    
    #admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    #biz model competition
    (r'^', include('bizmodelcomp.competition.urls')),

    #new competitions
    (r'^new/', include('bizmodelcomp.new_comp.urls')),

    #login, register, etc
    (r'^accounts/', include('bizmodelcomp.userhelper.urls')),
    (r'^no_permissions/', 'userhelper.views.noPermissions'),

    #apply to comp
    (r'^apply/', include('bizmodelcomp.entercompetition.urls')),

    (r'^export/', include('bizmodelcomp.export.urls')),                   

    #specific campaign clobbers
    (r'^echallenge/',
         'entercompetition.views.edit_pitch',
         {'competition_url': 'echallenge'}),

    #email
    (r'email/', include('bizmodelcomp.emailhelper.urls')),

    #data slicing & dicing, spreadsheets, etc
    (r'data/', include('bizmodelcomp.analytics.urls')),

    (r'^dashboard/', include('bizmodelcomp.dashboard.urls')),

    (r'^judge/', include('bizmodelcomp.judge.urls')),

    #flat pages
    (r'flat/(?P<site_copy_id>[a-zA-Z ]{1,30})/$', 'sitecopy.views.static_copy'),

    (r'^blog/', include('bizmodelcomp.blog.urls')),
)
