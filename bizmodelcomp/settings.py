# Django settings for bizmodelcomp project.
import socket
import os

is_local = False

local_windows = ['robfitz-PC', 'tugboat']
local_mac = ['mango', 'papaya', 'mango.local', 'Rob-Fitzpatricks-MacBook-Air.local']
test_server_hostnames = ['ip-10-122-193-156', 'ip-10-245-129-64']

filesystem = "UNIX"

if socket.gethostname() in local_windows:
    is_local = True
    filesystem = "WINDOWS"
elif socket.gethostname() in local_mac:
    is_local = True
    filesystem = "MAC"
else:
    is_test_server = socket.gethostname() in test_server_hostnames
    print 'Unrecognized hostname in settings.py: %s' % socket.gethostname()

DEBUG = is_local or is_test_server
#DEBUG = True
TEMPLATE_DEBUG = DEBUG

#kill switch for emailhelper
DISABLE_ALL_EMAIL = DEBUG

#whether new accounts are required to confirm
#their email before gaining their permissions.
#Email needs to be able to be sent for this to
#be a reasonable flag to set True, so is off on local
ACCOUNT_EMAIL_CONFIRM_REQUIRED = False#True
if is_local:
    ACCOUNT_EMAIL_CONFIRM_REQUIRED = False

ADMINS = (
    ('Rob Fitzpatrick', 'robftz@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'       # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'django_db_4'     # Or path to database file if using sqlite3.
DATABASE_USER = 'root'          # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

if is_local:
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = 'db_local'
    DATABASE_USER = ''


#sendgrid credentials required for emailhelper.send_email
EMAIL_USER = "robftz+nvana@gmail.com"
EMAIL_PASSWORD = "It's spam time!"
EMAIL_DEFAULT_FROM = "competitions@nvana.com"
EMAIL_LOG = '/var/www/bizmodelcomp/logs/email.log'
if filesystem == "WINDOWS":
    EMAIL_LOG = 'c:/www/bizmodelcomp/logs/email.log'
elif filesystem == "MAC":
    EMAIL_LOG = "/Users/%s/www/bizmodelcomp/logs/email.log" % os.getlogin()

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/bizmodelcomp/media/'
if filesystem == "WINDOWS":
    MEDIA_ROOT = 'c:/www/bizmodelcomp/media/'
elif filesystem == "MAC":
    MEDIA_ROOT = '../media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://nvana.com/media/'
if is_local:
    MEDIA_URL = 'http://localhost:8000/media/'
elif is_test_server:
    #MEDIA_URL = 'http://ec2-50-16-25-181.compute-1.amazonaws.com'
    MEDIA_URL = 'http://ec2-184-72-203-232.compute-1.amazonaws.com' 

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a # trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qj16npul8@&t&cec9pwic=vs=i#mke9te_wok^b!$#@r2$!0mo'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
)

APPEND_SLASH = True #from CommonMiddleware, makes either /page/ or /page valid

ROOT_URLCONF = 'bizmodelcomp.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "C:/www/bizmodelcomp/templates/",
    "/var/www/bizmodelcomp/templates/",
    "/Users/robfitz/www/bizmodelcomp/templates/",
    "/Users/thomasstone/www/bizmodelcomp/templates/",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'bizmodelcomp.competition',
    'bizmodelcomp.userhelper',
    'bizmodelcomp.entercompetition',
    'bizmodelcomp.sitecopy',
    'bizmodelcomp.judge',
    'bizmodelcomp.dashboard',
    'bizmodelcomp.emailhelper',
    'bizmodelcomp.new_comp',
    'bizmodelcomp.utils',
    'bizmodelcomp.blog',
    'south',
)

LOGIN_URL = "/accounts/login/"

AUTH_PROFILE_MODULE = "userhelper.UserProfile"

SCRIBD_API_KEY = "4jxkxjfj8efpubbj5q7i8"
SCRIBD_USER_ID = "pub-97515527877144087531"
SCRIBD_UPLOAD_URL = "http://api.scribd.com/api?method=docs.upload&api_key=%s&my_user_id=%s&access=private&secure=0&download_and_drm=view-only" % (SCRIBD_API_KEY, SCRIBD_USER_ID)

DATE_FORMAT = "M d, H:i"
