from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--@ha%wu@bx9#07=ugm_&nhe$jpxqfz1dwba)#5=ewkjc=6+31k"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


load_settings("geo")
load_settings("auth")
load_settings("api")
load_settings("restaurants")
load_settings("customers")
load_settings("inventory")
load_settings("orders")
load_settings("djext")
