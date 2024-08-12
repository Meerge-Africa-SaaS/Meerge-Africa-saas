# ruff: noqa: F405
from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure--@ha%wu@bx9#07=ugm_&nhe$jpxqfz1dwba)#5=ewkjc=6+31k"
)

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


load_settings("geo")
load_settings("restaurants")
load_settings("djext")
