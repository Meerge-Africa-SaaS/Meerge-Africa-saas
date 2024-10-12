from django.contrib import admin
from django import forms

from . import models


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"


class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = [
        "id",
        "customer",
        "delivery_address",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "id",
        "customer",
        "delivery_address",
        "created",
        "last_updated",
    ]


class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm
    list_display = [
        "last_name",
        "last_updated",
        "created",
        "address",
        "first_name",
    ]
    readonly_fields = [
        "last_name",
        "last_updated",
        "created",
        "address",
        "first_name",
    ]


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Customer, CustomerAdmin)
