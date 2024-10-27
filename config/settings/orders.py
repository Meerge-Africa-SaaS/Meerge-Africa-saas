from .base import INSTALLED_APPS

INSTALLED_APPS += [
    "orders.apps.OrdersConfig",
]
print(f"loading. .. {__file__}")