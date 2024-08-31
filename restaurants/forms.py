from django import forms

# from world.models import City
from core.models import User
from restaurants.models import Menu
from restaurants.models import MenuItem
from restaurants.models import Restaurant
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


class MenuForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = [
            "date_from",
            "name",
            "date_to",
        ]


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = models.MenuItem
        fields = [
            "name",
            "price",
            "menu",
        ]

    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        self.fields["menu"].queryset = Menu.objects.all()


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = [
            "address",
            "name",
            "city",
            "country",
            "owner",
        ]

    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        # self.fields["city"].queryset = City.objects.all()
        self.fields["owner"].queryset = User.objects.all()


class ChefForm(forms.ModelForm):
    class Meta:
        model = models.Chef
        fields = [
            "restaurants",
        ]

    def __init__(self, *args, **kwargs):
        super(ChefForm, self).__init__(*args, **kwargs)
        self.fields["restaurants"].queryset = Restaurant.objects.all()


class StaffForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = [
            "restaurants",
        ]

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields["restaurants"].queryset = Restaurant.objects.all()
