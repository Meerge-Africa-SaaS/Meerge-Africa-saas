# ruff: noqa: F405
from .base import *  # noqa: F403

# Django Xtensions
INSTALLED_APPS.extend(
    [
        # extensions
        "django_extensions",
    ]
)
GRAPH_MODELS = {
    "app_labels": [
        "core",
        "geo",
        "restaurant",
        # "inventory",
        # "orders",
    ],
    "group_models": True,
}
