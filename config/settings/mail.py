from .base import *
from .dev import DEBUG
try:
    if DEBUG:
        print("DEBUG MODE")
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
except:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "mail.kittchens.com"
EMAIL_PORT = 587

EMAIL_HOST_USER = "dev@kittchens.com"
EMAIL_HOST_PASSWORD = "8p([~su+2FgR"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
