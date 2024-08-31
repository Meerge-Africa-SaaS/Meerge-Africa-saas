from .base import *

# Django Xtensions
INSTALLED_APPS += [
    # extensions
    "django_extensions",
]
GRAPH_MODELS = {
    'app_labels': [
        "core",
        "geo",
        "restaurant",
        # "inventory",
        # "orders",
    ],
    'group_models': True,
}
