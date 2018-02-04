from .common import *

SECRET_KEY = 'g!u^)n56qhgmyv+2ey_9i6t!c3n_*fonp154d^++yzi3d_lw58'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'interactivemap',
        'USER': 'dwaxe',
        'PASSWORD': 'asdf1234',
        'HOST': 'localhost',
        'PORT': '',
    }
}