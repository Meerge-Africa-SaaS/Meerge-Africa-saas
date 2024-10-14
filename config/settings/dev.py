# ruff: noqa: F405
from django.conf import settings

from config.environ import getenv

from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .geo import *
    from .auth import *
    from .api import *
    from .restaurants import *
    from .customers import *
    from .inventory import *
    from .orders import *
    from .djext import *
    from .reload import *
    from .compressor import *
except ImportError as e:
    pass