from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms


class IngredientListView(generic.ListView):
    model = models.Ingredient
    form_class = forms.IngredientForm


class IngredientCreateView(generic.CreateView):
    model = models.Ingredient
    form_class = forms.IngredientForm


class IngredientDetailView(generic.DetailView):
    model = models.Ingredient
    form_class = forms.IngredientForm


class IngredientUpdateView(generic.UpdateView):
    model = models.Ingredient
    form_class = forms.IngredientForm
    pk_url_kwarg = "pk"


class IngredientDeleteView(generic.DeleteView):
    model = models.Ingredient
    success_url = reverse_lazy("restaurant_Ingredient_list")


class MenuListView(generic.ListView):
    model = models.Menu
    form_class = forms.MenuForm


class MenuCreateView(generic.CreateView):
    model = models.Menu
    form_class = forms.MenuForm


class MenuDetailView(generic.DetailView):
    model = models.Menu
    form_class = forms.MenuForm


class MenuUpdateView(generic.UpdateView):
    model = models.Menu
    form_class = forms.MenuForm
    pk_url_kwarg = "pk"


class MenuDeleteView(generic.DeleteView):
    model = models.Menu
    success_url = reverse_lazy("restaurant_Menu_list")


class MenuItemListView(generic.ListView):
    model = models.MenuItem
    form_class = forms.MenuItemForm


class MenuItemCreateView(generic.CreateView):
    model = models.MenuItem
    form_class = forms.MenuItemForm


class MenuItemDetailView(generic.DetailView):
    model = models.MenuItem
    form_class = forms.MenuItemForm


class MenuItemUpdateView(generic.UpdateView):
    model = models.MenuItem
    form_class = forms.MenuItemForm
    pk_url_kwarg = "pk"


class MenuItemDeleteView(generic.DeleteView):
    model = models.MenuItem
    success_url = reverse_lazy("restaurant_MenuItem_list")


class RestaurantListView(generic.ListView):
    model = models.Restaurant
    form_class = forms.RestaurantForm


class RestaurantCreateView(generic.CreateView):
    model = models.Restaurant
    form_class = forms.RestaurantForm


class RestaurantDetailView(generic.DetailView):
    model = models.Restaurant
    form_class = forms.RestaurantForm


class RestaurantUpdateView(generic.UpdateView):
    model = models.Restaurant
    form_class = forms.RestaurantForm
    pk_url_kwarg = "pk"


class RestaurantDeleteView(generic.DeleteView):
    model = models.Restaurant
    success_url = reverse_lazy("restaurant_Restaurant_list")


class ChefListView(generic.ListView):
    model = models.Chef
    form_class = forms.ChefForm


class ChefCreateView(generic.CreateView):
    model = models.Chef
    form_class = forms.ChefForm


class ChefDetailView(generic.DetailView):
    model = models.Chef
    form_class = forms.ChefForm


class ChefUpdateView(generic.UpdateView):
    model = models.Chef
    form_class = forms.ChefForm
    pk_url_kwarg = "pk"


class ChefDeleteView(generic.DeleteView):
    model = models.Chef
    success_url = reverse_lazy("restaurant_Chef_list")


class StaffListView(generic.ListView):
    model = models.Staff
    form_class = forms.StaffForm


class StaffCreateView(generic.CreateView):
    model = models.Staff
    form_class = forms.StaffForm


class StaffDetailView(generic.DetailView):
    model = models.Staff
    form_class = forms.StaffForm


class StaffUpdateView(generic.UpdateView):
    model = models.Staff
    form_class = forms.StaffForm
    pk_url_kwarg = "pk"


class StaffDeleteView(generic.DeleteView):
    model = models.Staff
    success_url = reverse_lazy("restaurant_Staff_list")
