from .common import *

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ['SECRET_KEY']

STATIC_URL = '/static/'
STATIC_ROOT = '/appstatic/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]