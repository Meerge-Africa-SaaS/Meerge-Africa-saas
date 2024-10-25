from django.contrib import admin
from django import forms

from . import models



class DeliveryRequestAdminForm(forms.ModelForm):
    class Meta:
        model = models.DeliveryRequest
        fields = "__all__"
        
        
class DeliveryRequestAdmin(admin.ModelAdmin):
    class Meta:
        model = models.DeliveryRequest
        fields = [
            "id",
            "order",
            "status"
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
admin.site.register(models.DeliveryRequest, DeliveryRequestAdmin)
