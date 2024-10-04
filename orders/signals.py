from django.db.models.signals import Signal


delivery_request_created = Signal(providing_args=["instance", "created"])