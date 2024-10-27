# ruff: noqa: F405
from .base import *  # noqa: F403

INSTALLED_APPS.extend(
    [
        "restaurants.apps.RestaurantsConfig",
    ]
)
print(f"loading. .. {__file__}")