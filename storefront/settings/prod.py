import os
from .common import *
import dj_database_url

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

ALLOWED_HOSTS = ["joestores-prod-1d75a0612d5e.herokuapp.com"]

DATABASES = {
    'default': dj_database_url.config()
}
