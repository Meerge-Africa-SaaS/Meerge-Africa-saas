from .base import *  # noqa: F403
TEMPLATE_EXTENSION = "html"
LOGIN_REDIRECT_URL = "actor_redirect"

INSTALLED_APPS += [  # noqa: F405
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
    "invitations",
]

AUTHENTICATION_BACKENDS = [
    "core.CustomFiles.CustomBackend.EmailAuthBackend",
    "core.CustomFiles.CustomBackend.PhoneAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "core.backends.EmailBackend"
]

print(f"loading. .. {__file__}")