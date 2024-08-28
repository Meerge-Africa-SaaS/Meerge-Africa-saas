from django.contrib import admin
from django import forms

from . import models


class IngredientAdminForm(forms.ModelForm):
    class Meta:
        model = models.Ingredient
        fields = "__all__"


class IngredientAdmin(admin.ModelAdmin):
    form = IngredientAdminForm
    list_display = [
        "last_updated",
        "name",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "name",
        "created",
    ]


class MenuAdminForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = "__all__"


class MenuAdmin(admin.ModelAdmin):
    form = MenuAdminForm
    list_display = [
        "date_from",
        "created",
        "name",
        "date_to",
        "last_updated",
    ]
    readonly_fields = [
        "date_from",
        "created",
        "name",
        "date_to",
        "last_updated",
    ]


class MenuItemAdminForm(forms.ModelForm):
    class Meta:
        model = models.MenuItem
        fields = "__all__"


class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemAdminForm
    list_display = [
        "name",
        "price",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "name",
        "price",
        "created",
        "last_updated",
    ]


class RestaurantAdminForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = "__all__"


class RestaurantAdmin(admin.ModelAdmin):
    form = RestaurantAdminForm
    list_display = [
        "address",
        "created",
        "name",
        "last_updated",
    ]
    readonly_fields = [
        "address",
        "created",
        "name",
        "last_updated",
    ]


class ChefAdminForm(forms.ModelForm):
    class Meta:
        model = models.Chef
        fields = "__all__"


class ChefAdmin(admin.ModelAdmin):
    form = ChefAdminForm
    list_display = [
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class StaffAdminForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = "__all__"


class StaffAdmin(admin.ModelAdmin):
    form = StaffAdminForm
    list_display = [
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Menu, MenuAdmin)
admin.site.register(models.MenuItem, MenuItemAdmin)
admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Chef, ChefAdmin)
admin.site.register(models.Staff, StaffAdmin)
