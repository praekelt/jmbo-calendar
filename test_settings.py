from os.path import expanduser

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jmbo',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = (
    'jmbo_calendar',
    'jmbo',
    'photologue',
    'category',
    'likes',
    'secretballot',
    'publisher',
    'preferences',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sites',
    'south',
)

ROOT_URLCONF = 'jmbo_calendar.tests.urls'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'likes.middleware.SecretBallotUserIpUseragentMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

USE_TZ = True

SITE_ID = 1

STATIC_URL = '/static/'

CKEDITOR_UPLOAD_PATH = expanduser('~')

SOUTH_TESTS_MIGRATE = False

# Disable celery
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'
