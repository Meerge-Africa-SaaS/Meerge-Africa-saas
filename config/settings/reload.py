# ruff: noqa: F405
from .base import *  # noqa: F403

INSTALLED_APPS.append("django_browser_reload")
MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")
