import os
from os.path import expanduser


USE_TZ = True

TIME_ZONE = "Africa/Johannesburg"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "jmbo",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

INSTALLED_APPS = (
    "jmbo_calendar",
    "jmbo_calendar.tests",
    "jmbo",
    "photologue",
    "category",
    "django_comments",
    "likes",
    "secretballot",
    "pagination",
    "preferences",
    "sites_groups",

    # Django apps can be alphabetic
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.humanize",
    "django.contrib.sites",

    # These apps have no templates
    "crum",
    "layers"
)

ROOT_URLCONF = "jmbo_calendar.tests.urls"

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "likes.middleware.SecretBallotUserIpUseragentMiddleware",
    "pagination.middleware.PaginationMiddleware",
)

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.template.context_processors.request",
    "django.contrib.messages.context_processors.messages",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.realpath(os.path.dirname(__file__)) + "/../templates/",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": TEMPLATE_CONTEXT_PROCESSORS,
        },
        "loaders": [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ]
    },
]


SITE_ID = 1

STATIC_URL = "/static/"

# Disable celery
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = "memory"

SECRET_KEY = "SECRET_KEY"

DEBUG = True

REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning"
}

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
