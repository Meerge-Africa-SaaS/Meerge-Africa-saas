# ruff: noqa: F403,F405
from .base import *

DEBUG = False

try:
    from .local import *  # type: ignore
except ImportError:
    pass
print(f"loading. .. {__file__}")