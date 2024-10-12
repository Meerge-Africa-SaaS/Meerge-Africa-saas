# ruff: noqa: F405
from config.environ import getenv
#from mail import EMAIL_BACKEND, EMAIL_PORT, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS
from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = getenv("EMAIL_HOST")#'smtp.gmail.com'#
EMAIL_PORT = 587#getenv("EMAIL_PORT")
EMAIL_HOST_USER = getenv("EMAIL_HOST_USER")#'crownprincesamuelaadeyemo@gmail.com'#
EMAIL_HOST_PASSWORD = getenv("EMAIL_HOST_PASSWORD")#'tkkt kzsu oqgy xzkc'#
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

load_settings("geo")
load_settings("auth")
load_settings("api")
load_settings("restaurants")
load_settings("customers")
load_settings("inventory")
load_settings("orders")
load_settings("djext")
load_settings("reload")
load_settings("compressor")
