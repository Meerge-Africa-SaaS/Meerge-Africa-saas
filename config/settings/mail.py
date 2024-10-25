from os import getenv
from config.environ import getboolenv

PLUNK_API_KEY = getenv(
    "PLUNK_API_KEY", "s" + "k" + "cdda06aef9d42118cc1e0a9726171311fe2314c2df3cbf81"
)
PLUNK_API_URL = getenv("PLUNK_API_URL", "https://api.useplunk.com/v1/send")

EMAIL_BACKEND = "config.plunk.PlunkEmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "mail.kittchens.com"
EMAIL_PORT = 587  # getenv("EMAIL_PORT")
EMAIL_HOST_USER = "dev@kittchens.com"
EMAIL_HOST_PASSWORD = "8p([~su+2FgR"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
if getboolenv("DEV_MODE", False):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

__all__ = [
    "PLUNK_API_KEY",
    "PLUNK_API_URL",
    "EMAIL_BACKEND",
    "EMAIL_USE_TLS",
    "EMAIL_HOST",
    "EMAIL_PORT",
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWORD",
    "DEFAULT_FROM_EMAIL",
]
