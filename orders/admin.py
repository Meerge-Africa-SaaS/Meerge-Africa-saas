from django.contrib import admin
from django import forms

from . import models


class DeliveryAgentAdminForm(forms.ModelForm):
    class Meta:
        model = models.DeliveryAgent
        fields = "__all__"


class DeliveryAgentAdmin(admin.ModelAdmin):
    form = DeliveryAgentAdminForm
    list_display = [
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


admin.site.register(models.DeliveryAgent, DeliveryAgentAdmin)
