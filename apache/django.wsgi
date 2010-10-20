import os
import sys

sys.path.append('/var/www/bizmodelcomp')
sys.path.append('/var/www/bizmodelcomp/bizmodelcomp')

os.environ['DJANGO_SETTINGS_MODULE'] = 'bizmodelcomp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
