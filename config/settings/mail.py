# ruff: noqa:F403
from config.env import getenv, getintenv
from config.settings import DJANGO_ENV


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
if DJANGO_ENV == "production":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_HOST = getenv("EMAIL_HOST")
    EMAIL_PORT = getintenv("EMAIL_PORT")
    EMAIL_HOST_USER = getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = getenv("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

print(f"DEBUG: email backend '{EMAIL_BACKEND}'")
