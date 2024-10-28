"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.settings import get_settings_module, load_dotenv_files


os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_settings_module())
load_dotenv_files()
application = get_wsgi_application()
