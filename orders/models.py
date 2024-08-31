from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
User = get_user_model()

class DeliveryAgent(User):
    
    address = models.ForeignKey("cities_light.Country", on_delete=models.SET_NULL, null=True, blank=True)
    # Fields
    # created = models.DateTimeField(auto_now_add=True, editable=False)
    # last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("orders_DeliveryAgent_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("orders_DeliveryAgent_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("orders_DeliveryAgent_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("orders_DeliveryAgent_htmx_delete", args=(self.pk,))
