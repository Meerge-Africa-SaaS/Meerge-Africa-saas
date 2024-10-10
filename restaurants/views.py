import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models


class EmailVerificationView(generic.TemplateView):
    template_name = "registration/restaurant/email_verification.html"


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


class MenuCategoryListView(LoginRequiredMixin, generic.ListView):
    model = models.MenuCategory
    form_class = forms.MenuCategoryForm


class MenuCategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.MenuCategory
    form_class = forms.MenuCategoryForm


class MenuCategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.MenuCategory
    form_class = forms.MenuCategoryForm


class MenuCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.MenuCategory
    form_class = forms.MenuCategoryForm
    pk_url_kwarg = "pk"


class MenuCategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.MenuCategory
    success_url = reverse_lazy("restaurant_MenuCategory_list")


class MenuListView(LoginRequiredMixin, generic.ListView):
    model = models.Menu
    form_class = forms.ViewMenuForm


class MenuCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Menu
    form_class = forms.MenuForm


class MenuDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Menu
    form_class = forms.ViewMenuForm


class MenuUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Menu
    form_class = forms.MenuForm
    pk_url_kwarg = "pk"


class MenuDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Menu
    success_url = reverse_lazy("restaurant_Menu_list")


class AddOnListView(LoginRequiredMixin, generic.ListView):
    model = models.AddOn
    form_class = forms.ViewAddOnForm


class AddOnCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.AddOn
    form_class = forms.AddOnForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AddOnDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.AddOn
    form_class = forms.ViewAddOnForm


class AddOnUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.AddOn
    form_class = forms.AddOnForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class AddOnDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.AddOn
    success_url = reverse_lazy("MenuItem")


class MenuItemListView(LoginRequiredMixin, generic.ListView):
    model = models.MenuItem
    form_class = forms.OwnerViewMenuItemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MenuItemCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.MenuItem
    form_class = forms.MenuItemForm
    template_name = "menuitem_create.html"
    # success_url =

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MenuItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.MenuItem
    form_class = forms.GeneralViewMenuItemForm


class MenuItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.MenuItem
    form_class = forms.MenuItemForm
    pk_url_kwarg = "pk"
    template_name = "menuitem_update.html"
    # success_url =

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MenuItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.MenuItem
    success_url = reverse_lazy("restaurant_MenuItem_list")
    template_name = "menuitem_delete.html"
    # success_url =

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class RestaurantListView(generic.ListView):
    model = models.Restaurant
    form_class = forms.RestaurantForm


class RestaurantCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Restaurant
    form_class = forms.RestaurantForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class RestaurantDetailView(generic.DetailView):
    model = models.Restaurant
    form_class = forms.RestaurantForm


class RestaurantUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Restaurant
    form_class = forms.RestaurantForm
    pk_url_kwarg = "pk"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class RestaurantDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Restaurant
    success_url = reverse_lazy("restaurant_Restaurant_list")


""" 
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
 """


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
