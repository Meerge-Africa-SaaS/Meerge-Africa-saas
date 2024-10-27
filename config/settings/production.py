# ruff: noqa: F403,F405,E402
from config.env import getlistenv, getenv
from .base import *

DEBUG = True
ALLOWED_HOSTS =  getlistenv("DJANGO_ALLOWED_HOSTS", [])
SECRET_KEY = getenv("DJANGO_SECRET_KEY")

try:
    from .local import *  # type: ignore
except ImportError:
    pass

from .geo import *
from .auth import *
from .mail import *
from .api import *
from .banking import *
from .restaurants import *
from .customers import *
from .inventory import *
from .orders import *
from .djext import *
from .reload import *
from .compressor import *