from django.contrib import admin
from django import forms

from . import models


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = "__all__"


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = [
        "created",
        "name",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "name",
        "last_updated",
    ]


class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = "__all__"


class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    list_display = [
        "last_updated",
        "unit_of_measure",
        "name",
        "id",
        "price",
        "created",
        "expiry_date",
    ]
    readonly_fields = [
        "last_updated",
        "unit_of_measure",
        "name",
        "id",
        "price",
        "created",
        "expiry_date",
    ]


class StockAdminForm(forms.ModelForm):
    class Meta:
        model = models.Stock
        fields = "__all__"


class StockAdmin(admin.ModelAdmin):
    form = StockAdminForm
    list_display = [
        "quantity",
        "product_name",
      
    ]


class SupplierAdminForm(forms.ModelForm):
    class Meta:
        model = models.Supplier
        fields = "__all__"


class SupplierAdmin(admin.ModelAdmin):
    form = SupplierAdminForm
    list_display = [
        "id",
        "created",
        "name",
        "owner",
        "email",
        "last_updated",
    ]
    readonly_fields = [
        "id",
        "created",
        "name",
        "owner",
        "last_updated",
        "email",
        "phone_number",
        "cac_reg_number",
        "cac_certificate",
        "business_license",
        "category",
        "profile_img",
        "cover_img",
        "address",
        "city"
    ]


class SupplyManagerAdminForm(forms.ModelForm):
    class Meta:
        model = models.SupplyManager
        fields = "__all__"


class SupplyManagerAdmin(admin.ModelAdmin):
    form = SupplyManagerAdminForm
    list_display = [
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Stock, StockAdmin)
admin.site.register(models.Supplier, SupplierAdmin)
admin.site.register(models.SupplyManager, SupplyManagerAdmin)
