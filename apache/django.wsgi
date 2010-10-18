import os
import sys

sys.path.append('/var/www/bizmodelcomp')
sys.path.append('/var/www/bizmodelcomp/bizmodelcomp')

try:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'bizmodelcomp.settings'
except:
    print 'awooooooga'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
