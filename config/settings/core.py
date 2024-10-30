from .base import *

INSTALLED_APPS += [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
]

AUTHENTICATION_BACKENDS = [
    "core.CustomFiles.CustomBackend.EmailAuthBackend",
    "core.CustomFiles.CustomBackend.PhoneAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "core.backends.EmailBackend"
]

print(f"loading. .. {__file__}")