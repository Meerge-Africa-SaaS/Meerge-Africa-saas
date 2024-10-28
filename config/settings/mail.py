from .base import *
LOCAL = os.getenv("LOCAL", False)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
if LOCAL:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = 587


EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

print(f"loading. .. {__file__}\n{LOCAL}\n{EMAIL_BACKEND}")
