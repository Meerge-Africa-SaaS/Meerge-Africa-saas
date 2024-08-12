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
        # "restaurant",
        # "world",
        # "customers",
        # "inventory",
        # "orders",
    ],
    "group_models": True,
}
