from .base import *
LOCAL = os.getenv("LOCAL", False)
try:
    if LOCAL:
        print(f"{LOCAL = }")
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
except:
    print(f"{LOCAL = }")
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "mail.kittchens.com"
EMAIL_PORT = 587

EMAIL_HOST_USER = "dev@kittchens.com"
EMAIL_HOST_PASSWORD = "8p([~su+2FgR"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
print(f"loading. .. {__file__}")