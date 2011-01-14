from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'blog.views.latest'),

    (r'^(?P<post_url>[-_0-9a-zA-Z]{1,200})/$', 
        'blog.views.post'),

)

