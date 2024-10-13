from django import forms

from . import models


class DeliveryRequestForm(forms.ModelForm):
    class Meta:
        model = models.DeliveryRequest
        fields = [
        "order",
        "status",
        "deliveryagent",
        ]

class DeliveryAgentForm(forms.ModelForm):
    class Meta:
        model = models.DeliveryAgent
        fields: list[str] = []
