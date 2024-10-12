from django.contrib import admin
from django import forms

from . import models



class DeliveryRequestAdminForm(forms.ModelForm):
    class Meta:
        model = models.DeliveryRequest
        fields = "__all__"


class DeliveryAgentAdmin(admin.ModelAdmin):
    form = DeliveryRequestAdminForm
    
    list_display = [
        "id",
        "status",
        "deliveryagent",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "id",
        "order",
        "status",
        "deliveryagent",
        "created",
        "last_updated",
    ]


class DeliveryAgentAdminForm(forms.ModelForm):

    class Meta:
        model = models.DeliveryAgent
        fields = "__all__"


class DeliveryAgentAdmin(admin.ModelAdmin):
    form = DeliveryAgentAdminForm
    list_display = [
        "id",
        "email",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "id",
        "email",
        "created",
        "last_updated",
    ]


admin.site.register(models.DeliveryAgent, DeliveryAgentAdmin)
