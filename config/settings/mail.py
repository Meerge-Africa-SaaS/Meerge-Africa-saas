from .base import *
from .dev import DEBUG
from config.local import local
LOCAL = local()
try:
    if DEBUG and LOCAL:
        print(f"DEBUG MODE: {LOCAL}")
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
except:
    print(f"DEBUG MODE: {LOCAL}")
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "mail.kittchens.com"
EMAIL_PORT = 587

EMAIL_HOST_USER = "dev@kittchens.com"
EMAIL_HOST_PASSWORD = "8p([~su+2FgR"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
