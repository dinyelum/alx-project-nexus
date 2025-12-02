import os
from .common import *

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

ALLOWED_HOSTS = ["joestores-prod-1d75a0612d5e.herokuapp.com"]
