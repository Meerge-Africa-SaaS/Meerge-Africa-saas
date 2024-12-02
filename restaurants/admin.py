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

class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = models.MenuCategory
        fields = "__all__"
        
class MenuCategoryAdmin(admin.ModelAdmin):
    form = MenuCategoryForm
    list_display = [
        "name",
        "description",
        "date_from",
        "date_to"
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
        "category",
        "restaurant",
        "name",
        "date_to",
        "last_updated",
    ]
    readonly_fields = [
        "date_from",
        "created",
        "name",
        "restaurant",
        "category",
        "date_to",
        "last_updated",
    ]


class AddOnAdminForm(forms.ModelForm):
    class Meta:
        model = models.AddOn
        fields = "__all__"
        

class AddOnAdmin(admin.ModelAdmin):
    form = AddOnAdminForm
    list_display = [
        "name",
        "price"
    ]
    readonly_fields = [
        "name",
        "price",
        "restaurant",
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
        "menu",
        "restaurant",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "menu",
        "restaurant",
        "add_ons",
        "name",
        "price",
        "portion",
        "size",
        "ingredient_details",
        "diet_type",
        "spice_level",
        "status",
        "nutritional_info_summary",
        "ready_in",
        "discount_percentage",
        "image",
        "video",
        "created",
        "last_updated",
    ]
    filter_horizontal = ('add_ons',)


class RestaurantCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = models.RestaurantCategory
        fields = "__all__"
        

class RestaurantCategoryAdmin(admin.ModelAdmin):
    form = RestaurantCategoryAdminForm
    list_display=[
        "name"
    ]
    readonly_fields=[
        "name",
        "description"
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
        "add_ons",
        "name",
        "email",
        "phone_number",
        "business_category",
        "business_reg_details",
        "cac_reg_number",
        "cac_certificate",
        "business_license",
        "last_updated",
        "profile_img",
        "cover_img",
        "custom_link",
    ]
   

class RestaurantStoreAdminForm(forms.ModelForm):
    class Meta:
        model = models.RestaurantStore
        fields = "__all__" 
        

class RestaurantStoreAdmin(admin.ModelAdmin):
    form = RestaurantStoreAdminForm
    list_display = [
        "name",
        "restaurant"
    ]
    ''' readonly_fields = [
        "restaurant",
        "name",
        "description",
        "image",
        "section_name"
    ] '''
    

class RestaurantStockAdminForm(forms.ModelForm):
    class Meta:
        model = models.RestaurantStock
        fields = "__all__"
        

class RestaurantStockAdmin(admin.ModelAdmin):
    form = RestaurantStockAdminForm
    list_display = [
        "category",
        "name",
        #"restaurant",
        "store",
    ]
    ''' readonly_fields = [
        #"category",
        #"name",
        #"image",
        #"stock_type",
        #"purchasing_price",
        #"quantity",
        #"measuring_unit",
        #"restaurant",
        #"store",
    ] '''
    
    
''' 

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

 '''
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
admin.site.register(models.AddOn, AddOnAdmin)
admin.site.register(models.MenuItem, MenuItemAdmin)
admin.site.register(models.MenuCategory, MenuCategoryAdmin)
admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.RestaurantStore, RestaurantStoreAdmin)
admin.site.register(models.RestaurantStock, RestaurantStockAdmin)
#admin.site.register(models.Chef, ChefAdmin)
admin.site.register(models.Staff, StaffAdmin)
