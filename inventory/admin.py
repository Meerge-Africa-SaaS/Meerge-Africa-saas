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
        "id",
        "created", 
        "name",
        "last_updated",
    ]
    readonly_fields = [
        "id",
        "created",
        "last_updated",
    ]
    
    
class ItemCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = models.ItemCategory
        fields = "__all__"


class ItemCategoryAdmin(admin.ModelAdmin):
    form = ItemCategoryAdminForm
    list_display = [
        "id",
        "created",
        "name", 
        "last_updated",
    ]
    readonly_fields = [
        "id",
        "created",
        "last_updated",
    ]


class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = "__all__"


class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    list_display = [
        "id",
        "name",
        "category",
        "stock",
        "unit_of_measure",
        "price",
        "expiry_date",
        "created",
        "last_updated"
    ]
    readonly_fields = [
        "id",
        "created",
        "last_updated"
    ]


class StockAdminForm(forms.ModelForm):
    class Meta:
        model = models.Stock
        fields = "__all__"


class StockAdmin(admin.ModelAdmin):
    form = StockAdminForm
    list_display = [
        "id",
        "supplier",
        "product_name",
        "SKU_number",
        "product_category",
        "quantity",
        "unit_available",
        "price",
        "created",
        "last_updated"
    ]
    readonly_fields = [
        "id",
        "created",
        "last_updated"
    ]


class SupplierAdminForm(forms.ModelForm):
    class Meta:
        model = models.Supplier
        fields = "__all__"


class SupplierAdmin(admin.ModelAdmin):
    form = SupplierAdminForm
    list_display = [
        "id",
        "name",
        "owner",
        "email",
        "phone_number",
        "address",
        "created",
        
    ]
    readonly_fields = [
        "id",
        "created",
        
    ]


class SupplyManagerAdminForm(forms.ModelForm):
    class Meta:
        model = models.SupplyManager
        fields = "__all__"


class SupplyManagerAdmin(admin.ModelAdmin):
    form = SupplyManagerAdminForm
    list_display = [
        "id", 
        "supply_business",
        "account_details",
        "created",
        "last_updated"
    ]
    readonly_fields = [
        "id",
        "created",
        "last_updated"
    ]


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.ItemCategory, ItemCategoryAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Stock, StockAdmin)
admin.site.register(models.Supplier, SupplierAdmin)
admin.site.register(models.SupplyManager, SupplyManagerAdmin)
