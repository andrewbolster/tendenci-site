import os.path
from os import environ
import dj_database_url

# go one level up
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_ADDONS_PATH = os.path.join(PROJECT_ROOT, 'addons')

# Helper lambda for gracefully degrading environmental variables:
env = lambda e, d: environ[e] if e in environ else d

# Load the .env file into the os.environ for secure information
try:
    env_file = open(os.path.join(PROJECT_ROOT, '.env'), 'r')
    for line in env_file.readlines():
        env_key = line.rstrip().split("=")[0]
        if env_key:
            env_key = env_key.rstrip()
            # set the environment variable to the value with the start and
            # end quotes taken off.
            env_value = ''.join(line.rstrip().split("=")[1:]).strip()
            if env_value:
                if env_value[0] == "'" or env_value[0] == '"':
                    env_value = env_value[1:-1]

                environ[env_key] = env_value
    env_file.close()
except:
    # no .env file or errors in the file
    pass


from tendenci.settings import *


ADMINS = ()

MANAGERS = ADMINS

DEBUG = env('DEBUG', False)
TEMPLATE_DEBUG = env('DEBUG', DEBUG)

ROOT_URLCONF = 'conf.urls'

SECRET_KEY = env('SECRET_KEY', 's6324SF3gmt051wtbazonjm4fg0+icbx3rjzcDGFHDR67ua6i')

INSTALLED_APPS += (
    'gunicorn',
)


# -------------------------------------- #
# DATABASES
# -------------------------------------- #

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'tendenci',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '',
#         'OPTIONS': {'autocommit': True},
#     }
# }

DATABASES = env('DATABASES', {'default': dj_database_url.config(default='postgres://localhost')})

DATABASES['default']['OPTIONS'] = {'autocommit': True}


# -------------------------------------- #
# DEBUG OPTIONS
# -------------------------------------- #

if env('SENTRY_DSN', None):
    INSTALLED_APPS += ('raven.contrib.django',)

if env('INTERNAL_IPS', None):
    INTERNAL_IPS = [env('INTERNAL_IPS', '127.0.0.1')]

if env('DEBUG_TOOLBAR', None):
    def always_show_toolbar(request):
        return True

    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT_REDIRECTS": False,
        "SHOW_TOOLBAR_CALLBACK": always_show_toolbar,
    }


# -------------------------------------- #
# SOLR
# -------------------------------------- #

HAYSTACK_URL = env('WEBSOLR_URL', 'http://localhost')

HAYSTACK_SEARCH_ENGINE = env('HAYSTACK_SEARCH_ENGINE', 'solr')
HAYSTACK_SOLR_URL = HAYSTACK_URL


# -------------------------------------- #
# THEMES
# -------------------------------------- #

TEMPLATE_DIRS += (os.path.join(PROJECT_ROOT, "themes"),)
THEMES_DIR = os.path.join(PROJECT_ROOT, 'themes')

# ORIGINAL_THEMES_DIR is used when USE_S3_STORAGE==True
ORIGINAL_THEMES_DIR = THEMES_DIR
LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'themes'),)


# -------------------------------------- #
# STATIC MEDIA
# -------------------------------------- #

STATICFILES_DIRS += (
    #('media', os.path.join(PROJECT_ROOT, 'site_media/media')),
#    THEMES_DIR,
)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

# Stock static media files and photos from the URL below
# are licensed by Ed Schipul as Creative Commons Attribution
# http://creativecommons.org/licenses/by/3.0/
#
# The full image set is available online at
# http://tendenci.com/photos/set/3/

STOCK_STATIC_URL = '//d15jim10qtjxjw.cloudfront.net/master-90/'

TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.static', )

# s3 storeage
AWS_LOCATION = env('AWS_LOCATION', '')    # this is usually your site name
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', '')

USE_S3_STORAGE = all([AWS_LOCATION,
                    AWS_ACCESS_KEY_ID,
                    AWS_SECRET_ACCESS_KEY,
                    AWS_STORAGE_BUCKET_NAME])

if USE_S3_STORAGE:

    INSTALLED_APPS += (
                       'storages',
                       's3_folder_storage',
                       )
    # media
    DEFAULT_S3_PATH = "%s/media" % AWS_LOCATION
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'

    # static
    STATIC_S3_PATH = "%s/static" % AWS_LOCATION
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'

    # themes
    THEME_S3_PATH = "%s/themes" % AWS_LOCATION

    S3_ROOT_URL = 'https://s3.amazonaws.com'
    S3_SITE_ROOT_URL = '%s/%s/%s' % (S3_ROOT_URL, AWS_STORAGE_BUCKET_NAME, AWS_LOCATION)

    MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
    MEDIA_URL = '%s/media/' % S3_SITE_ROOT_URL

    S3_STATIC_ROOT = "/%s/" % STATIC_S3_PATH
    STATIC_URL = '%s/static/' % S3_SITE_ROOT_URL

    #TINYMCE_JS_ROOT = STATIC_ROOT + 'tinymce'
    #TINYMCE_JS_URL = STATIC_URL + 'tinymce/tiny_mce.js'

    S3_THEME_ROOT = "/%s/" % THEME_S3_PATH
    THEMES_DIR = '%s/themes' % S3_SITE_ROOT_URL

    AWS_QUERYSTRING_AUTH = False


SSL_ENABLED = env('SSL_ENABLED', False)

# ---------------------------------------#
# PAYMENT GATEWAY
# ---------------------------------------#
# authorizenet, firstdata (the first two)
MERCHANT_LOGIN = env('MERCHANT_LOGIN', '')
MERCHANT_TXN_KEY = env('MERCHANT_TXN_KEY', '')
AUTHNET_MD5_HASH_VALUE = env('AUTHNET_MD5_HASH_VALUE', '')
AUTHNET_POST_URL = env('AUTHNET_POST_URL', AUTHNET_POST_URL)

# paypalpayflowlink
PAYPAL_MERCHANT_LOGIN = env('PAYPAL_MERCHANT_LOGIN', '')
PAYFLOWLINK_PARTNER = env('PAYFLOWLINK_PARTNER', 'PayPal')

# stripe
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY', '')


# -------------------------------------- #
# CACHE
# -------------------------------------- #

SITE_CACHE_KEY = env('SECRET_KEY', 'sitename-here')
SITE_SETTINGS_KEY_ENV = env('SITE_SETTINGS_KEY', None)
if SITE_SETTINGS_KEY_ENV:
    SITE_SETTINGS_KEY = SITE_SETTINGS_KEY_ENV

CACHE_PRE_KEY = SITE_CACHE_KEY
JOHNNY_MIDDLEWARE_KEY_PREFIX = SITE_CACHE_KEY

LOCAL_CACHE_PATH = env('LOCAL_CACHE_PATH', os.path.join(PROJECT_ROOT, "cache"))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': LOCAL_CACHE_PATH,
        'OPTIONS': {'MAX_ENTRIES': 1000000},
    }
}

# MEMCACHE
# https://addons.heroku.com/memcache

MEMCACHE_SERVERS = env('MEMCACHE_SERVERS', '')

if MEMCACHE_SERVERS:
    CACHES = {
        'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        }
    }

# MEMCACHIER
# https://addons.heroku.com/memcachier

MEMCACHIER_SERVERS = env('MEMCACHIER_SERVERS', '')

if MEMCACHIER_SERVERS:
    os.environ['MEMCACHE_SERVERS'] = MEMCACHIER_SERVERS
    os.environ['MEMCACHE_USERNAME'] = env('MEMCACHIER_USERNAME', '')
    os.environ['MEMCACHE_PASSWORD'] = env('MEMCACHIER_PASSWORD', '')

    CACHES = {
        'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'LOCATION': MEMCACHIER_SERVERS,
            'BINARY': True,
        }
    }

# Caching defaults

CACHES['default']['TIMEOUT'] = 604800  # 1 week
CACHES['default']['JOHNNY_CACHE'] = True


# -------------------------------------- #
# MAIL
# -------------------------------------- #

EMAIL_USE_TLS = env('EMAIL_USE_TLS', True)
EMAIL_HOST = env('EMAIL_HOST', None)
EMAIL_PORT = env('EMAIL_PORT', None)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', None)

EMAIL_BACKEND = env('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

# SENDGRID

SENDGRID_USERNAME = env('SENDGRID_USERNAME', '')
SENDGRID_PASSWORD = env('SENDGRID_PASSWORD', '')

USE_SENDGRID = all([SENDGRID_USERNAME, SENDGRID_PASSWORD])

if USE_SENDGRID:
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = SENDGRID_USERNAME
    EMAIL_HOST_PASSWORD = SENDGRID_PASSWORD
    EMAIL_PORT = '587'

# MAILGUN

MAILGUN_SMTP_SERVER = env('MAILGUN_SMTP_SERVER', '')
MAILGUN_SMTP_LOGIN = env('MAILGUN_SMTP_LOGIN', '')
MAILGUN_SMTP_PASSWORD = env('MAILGUN_SMTP_PASSWORD', '')
MAILGUN_SMTP_PORT = env('MAILGUN_SMTP_PORT', '')

USE_MAILGUN = all([MAILGUN_SMTP_SERVER,
                MAILGUN_SMTP_LOGIN,
                MAILGUN_SMTP_PASSWORD,
                MAILGUN_SMTP_PORT])

if USE_MAILGUN:
    EMAIL_USE_TLS = True
    EMAIL_HOST = MAILGUN_SMTP_SERVER
    EMAIL_HOST_USER = MAILGUN_SMTP_LOGIN
    EMAIL_HOST_PASSWORD = MAILGUN_SMTP_PASSWORD
    EMAIL_PORT = MAILGUN_SMTP_PORT


DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
SERVER_EMAIL = env('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# -------------------------------------- #
# CAMPAIGN MONITOR
# -------------------------------------- #

CAMPAIGNMONITOR_URL = env('CAMPAIGNMONITOR_URL', '')
CAMPAIGNMONITOR_API_KEY = env('CAMPAIGNMONITOR_API_KEY', '')
CAMPAIGNMONITOR_API_CLIENT_ID = env('CAMPAIGNMONITOR_API_CLIENT_ID', '')


# THIS MUST BE AT THE END!
# -------------------------------------- #
# ADDONS
# -------------------------------------- #

DEFAULT_INSTALLED_APPS = INSTALLED_APPS
from tendenci.core.registry.utils import update_addons
INSTALLED_APPS = update_addons(INSTALLED_APPS)
