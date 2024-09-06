from django import forms

from . import models


class DeliveryAgentForm(forms.ModelForm):
    class Meta:
        model = models.DeliveryAgent
        fields: list[str] = []
