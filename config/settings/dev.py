import os
from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

try:
    from .restaurants import *
    from .core import *
    from .sre import *
    from .geo import *
    from .banking import *
    from .auth import *
    from .mail import *
    from .api import *
    from .customers import *
    from .inventory import *
    from .orders import *
    from .djext import *
    from .reload import *
    from .compressor import *
    from .cloudinary import *
except Exception as e:
    print(f"error loading. .. {__file__}")
    print(e)

