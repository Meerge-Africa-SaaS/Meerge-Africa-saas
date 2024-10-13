# ruff: noqa: F405
from .base import *  # noqa: F403

INSTALLED_APPS.append("compressor")

COMPRESS_ROOT = os.path.join(BASE_DIR, "static")

COMPRESS_ENABLED = True

try:
    STATICFILES_FINDERS.append("compressor.finders.CompressorFinder")  # type: ignore
except NameError:
    STATICFILES_FINDERS = ["compressor.finders.CompressorFinder"]
