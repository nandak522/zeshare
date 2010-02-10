import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('NandaKishore', 'madhav.bnk@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'zeshare'             # Or path to database file if using sqlite3.
DATABASE_USER = 'zeshare'             # Not used with sqlite3.
DATABASE_PASSWORD = 'zeshare'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

ROOT_PATH = os.getcwd()

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/site_media/' % ROOT_PATH

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'm%xe#uy25qu=1+hikz5)@^e)0&9@a1=3ucg731r@)6e+2yrw0#'

EMAIL_SUBJECT_PREFIX = '[ZeShare] '

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
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTH_PROFILE_MODULE='users.UserProfile'

AUTHENTICATION_BACKENDS = ('utils.authbackend.EmailBackend',)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'zeshare.urls'

TEMPLATE_DIRS = (
    "%s/templates" % ROOT_PATH,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'users',
    'quest',
    'extensions',
    'utils',
    'tagging',
    'debug_toolbar'
)

ADMIN_USERNAME = 'zeadmin'
ADMIN_PASSWORD = 'zeadmin'

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

FORCE_LOWERCASE_TAGS = True