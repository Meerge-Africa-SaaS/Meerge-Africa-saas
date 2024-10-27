# ruff: noqa: F405,F403,E402
from config.env import getenv
#from mail import EMAIL_BACKEND, EMAIL_PORT, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS
from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

from .geo import *
from .auth import *
from .mail import *
from .api import *
from .banking import *
from .restaurants import *
from .customers import *
from .inventory import *
from .orders import *
from .djext import *
from .reload import *
from .compressor import *