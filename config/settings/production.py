# ruff: noqa: F405,F403,E402
from .base import *

DEBUG = False

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

try:
    from .local import *  # type: ignore
except ImportError:
    pass
