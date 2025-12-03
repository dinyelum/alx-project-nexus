from .common import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+i476^((cn^^p^pv$31@3*e+zpfm=ar-c78e2p+0b=lg59uw3k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TESTING = "test" in sys.argv or "PYTEST_VERSION" in os.environ

ALLOWED_HOSTS = []

INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # if you have a global static folder
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
