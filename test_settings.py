from foundry.settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'calendar',
        'USER': 'test',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Need this last line until django-setuptest is improved.
