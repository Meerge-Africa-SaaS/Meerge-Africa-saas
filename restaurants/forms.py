import os

from django import forms

# from world.models import City
from core.models import User
from restaurants.models import (
    Menu,
    MenuCategory,
    MenuItem,
    Restaurant,
    RestaurantCategory,
)

from . import models


class IngredientForm(forms.ModelForm):
    class Meta:
        model = models.Ingredient
        fields = [
            "name",
            "menu_item",
        ]

    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        self.fields["menu_item"].queryset = MenuItem.objects.all()


class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = models.MenuCategory
        fields = ["name", "description", "date_from", "date_to"]


class MenuForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = ["date_from", "name", "date_to", "category", "restaurant"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("user", None)
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"].queryset = Restaurant.objects.filter(owner=self.user)
        self.fields["category"].queryset = RestaurantCategory.objects.all()


class ViewMenuForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = ["date_from", "name", "date_to", "category", "restaurant"]

    def __init__(self, *args, **kwargs):
        super(ViewMenuForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["restaurant"].queryset = Restaurant.objects.filter(
                id=self.instance.restaurant.id
            )
            self.fields["category"].queryset = MenuCategory.objects.filter(
                category_ID=self.instance.category.category_ID
            )
        else:
            self.fields["restaurant"].queryset = Restaurant.objects.none()
            self.fields["category"].queryset = MenuCategory.objects.none()


class AddOnForm(forms.ModelForm):
    class Meta:
        model = models.AddOn
        fields = [
            "restaurant",
            "name",
            "price",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(AddOnForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"] = Restaurant.objects.filter(owner=self.user)

    def clean_name(self):
        name = self.cleaned_data("name")
        if not isinstance(name, str):
            raise forms.ValidationError("Value input must be alphabet only.")
        return name

    def clean_price(self):
        price = self.cleaned_data("price")
        if not price:
            price = 0
        if price and price < 0:
            raise forms.ValidationError("Price cannot be less than zero.")
        return price


class ViewAddOnForm(forms.ModelForm):
    class Meta:
        model = models.AddOn
        fields = ["restaurant", "name", "price"]

    def __init__(self, *args, **kwargs):
        super(ViewAddOnForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"] = Restaurant.objects.filter(add_ons=self.instance.pk)


class MenuItemForm(forms.ModelForm):
    # Adding the password field
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        help_text="Enter your password to confirm this action",
    )

    class Meta:
        model = models.MenuItem
        fields = [
            "menu",
            "restaurant",
            "name",
            "price",
            "portion",
            "size",
            "ingredient_details",
            "diet_type",
            "spice_level",
            "status",
            "nutritional_info_summary",
            "add_ons",
            "ready_in",
            "discount_percentage",
            "image",
            "video",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(MenuItemForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"].queryset = Restaurant.objects.filter(owner=self.user)

    def clean_restaurant(self):
        restaurant = self.cleaned_data("restaurant")
        if restaurant.owner != self.user:
            raise forms.ValidationError("You do not own this restaurant")
        return restaurant

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.user.check_password(password):
            raise forms.ValidationError("Incorrect Password")
        return password

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise forms.ValidationError("Forms cannot be negative")

    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data.get("discount_percentage")
        if discount_percentage < 0:
            raise forms.ValidationError("Discount Percentage cannot be negative")
        return discount_percentage


class OwnerViewMenuItemForm(forms.ModelForm):
    class Meta:
        model = models.MenuItem
        fields = [
            "name",
            "price",
            "menu",
            "restaurant",
            "portion",
            "size",
            "status",
            "ready_in",
            "add_ons",
            "ingredient_details",
            "image",
            "video",
            "diet_type",
            "spice_level",
            "nutritional_info_summary",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(OwnerViewMenuItemForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"].queryset = Restaurant.objects.filter(owner=self.user)
        if "restaurant" in self.fields:
            restaurant = self.fields["restaurant"]
        self.fields["menu"].queryset = Menu.objects.filter(restaurant=restaurant)

    def clean_restaurant(self):
        restaurant = self.cleaned_data("restaurants")
        if restaurant.owner != self.user:
            raise forms.ValidationError("You do not own this restaurant")
        return restaurant


class GeneralViewMenuItemForm(forms.ModelForm):
    class Meta:
        model = models.MenuItem
        fields = [
            "name",
            "price",
            "menu",
            "restaurant",
            "portion",
            "size",
            "status",
            "ready_in",
            "add_ons",
            "ingredient_details",
            "image",
            "video",
            "diet_type",
            "spice_level",
            "nutritional_info_summary",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(GeneralViewMenuItemForm, self).__init__(*args, **kwargs)
        if "restaurant" in self.fields:
            restaurant = self.fields["restaurant"]
        self.fields["menu"].queryset = Menu.objects.filter(restaurant=restaurant)


class RestaurantCategoryForm(forms.ModelForm):
    class Meta:
        model = models.RestaurantCategory
        fields = ["name", "description"]


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = [
            "address",
            "name",
            "email",
            "phone_number",
            "business_category",
            "business_reg_details",
            "cac_reg_number",
            "cac_certificate",
            "business_license",
            "profile_img",
            "cover_img",
            "city",
            "country",
            "owner",
            "add_ons",
            "custom_link",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(RestaurantForm, self).__init__(*args, **kwargs)
        # self.fields["city"].queryset = City.objects.all()
        #
        if self.instance.pk:
            self.fields["owner"].queryset = Restaurant.objects.filter(owner=self.user)

        else:
            self.fields["owner"].queryset = User.objects.all()

    def clean_custom_link(self):
        custom_link = self.cleaned_data.get("custom_link")
        if not custom_link:
            return custom_link
        if not custom_link.isalnum():
            raise forms.ValidationError("Special characters are not allowed.")
        if custom_link and custom_link < 3:
            raise forms.ValidationError(
                "Custom link tagname cannot be less than 3 characters"
            )
        if custom_link > 24:
            raise forms.ValidationError(
                "Custom link tagname cannot be more than 24 characters"
            )

        return custom_link


class GeneralViewRestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = [
            "address",
            "name",
            "email",
            "phone_number",
            "business_category",
            "business_reg_details",
            "cac_reg_number",
            "cac_certificate",
            "business_license",
            "profile_img",
            "cover_img",
            "city",
            "country",
            "owner",
            "add_ons",
            "custom_link",
        ]

    def __init__(self, *args, **kwargs):
        super(GeneralViewRestaurantForm, self).__init__(*args, **kwargs)
        # self.fields["city"].queryset = City.objects.all()
        self.fields["owner"].queryset = User.objects.all()
        self.fields["restaurant"] = Restaurant.objects.all()

    def clean_custom_link(self):
        custom_link = self.cleaned_data.get("custom_link")
        if not custom_link:
            pass
        if not custom_link.isalnum():
            raise forms.ValidationError("Special characters are not allowed.")
        if custom_link and custom_link < 3:
            raise forms.ValidationError(
                "Custom link tagname cannot be less than 3 characters"
            )
        if custom_link > 24:
            raise forms.ValidationError(
                "Custom link tagname cannot be more than 24 characters"
            )

        return custom_link


""" 

class ChefForm(forms.ModelForm):
    class Meta:
        model = models.Chef
        fields = [
            "restaurants",
        ]

    def __init__(self, *args, **kwargs):
        super(ChefForm, self).__init__(*args, **kwargs)
        self.fields["restaurants"].queryset = Restaurant.objects.all()

 """



class StaffForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = [
            "restaurants",
        ]

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields["restaurants"].queryset = Restaurant.objects.all()


class RestaurantLogoForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = ["profile_img"]


class RestaurantCoverForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = ["cover_img"]
