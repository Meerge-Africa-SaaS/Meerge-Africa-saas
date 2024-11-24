import os
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from inventory.models import Category

from . import forms, models


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

    
class RestaurantStoreCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.RestaurantStore
    form_class = forms.RestaurantStoreForm
    template_name = "restaurants/components/create-store.html"
    success_url = ""
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs
    
    def form_valid(self, form: forms.RestaurantStoreForm):
        restaurant = form.cleaned_data["restaurant"]
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        section_name = form.cleaned_data["section_name"]
        
        form_saved = form.save(restaurant=restaurant, name=name, section_name=section_name, description=description)
        return HttpResponse(form_saved)
    
    

class RestaurantStoreUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.RestaurantStore
    form_class = forms.RestaurantStoreForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
    
class RestaurantStoreListView(LoginRequiredMixin, generic.ListView):
    model = models.RestaurantStore
    form_class = forms.RestaurantStoreForm
    template_name = "restaurants/components/restaurantstore_list.html"
    context_object_name = "restaurant_stores"
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["restaurant_stores"] = models.RestaurantStore.objects.filter(restaurant=self.kwargs["pk"])
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["restaurant_stores"] = models.RestaurantStore.objects.filter(restaurant=self.kwargs["pk"])
        return kwargs
    
    def get_queryset(self):
        return models.RestaurantStore.objects.filter(restaurant=self.kwargs["pk"])
    
class RestaurantStoreDetailView(generic.DetailView):
    model = models.RestaurantStore
    form_class = forms.RestaurantStoreForm
    template_name = "restaurants/pages/inventory/restaurantstore_detail_page.html"
    
    
class RestaurantStockListView(LoginRequiredMixin, generic.ListView):
    model = models.RestaurantStock
    form_class = forms.RestaurantStockForm
    
class RestaurantStockCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.RestaurantStock
    form_class = forms.RestaurantStockForm
    template_name = "restaurants/components/add-stock-item.html"
    success_url = None
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs
    
    def form_valid(self, form: form_class):
        super().form_valid(form)
        return JsonResponse({"status_code":200}, safe=False)
    ''' 
    def form_valid(self, form: form_class):
        store = form.cleaned_data["store"],
        category = form.cleaned_data["category"],
        name = form.cleaned_data["name"],
        purchasing_price = form.cleaned_data["purchasing_price"],
        quantity = form.cleaned_data["quantity"],
        measuring_unit = form.cleaned_data["measuring_unit"],
        low_stock_alert_unit = form.cleaned_data["low_stock_alert_unit"],
        expiry_date = form.cleaned_data["expiry_date"],
        print(store, category)
        form_saved = form.save(store=store, category=category.id, name=name, purchasing_price=purchasing_price, 
                               quantity=quantity, measuring_unit=measuring_unit, low_stock_alert_unit=low_stock_alert_unit, 
                               expiry_date=expiry_date)
        return HttpResponse(form_saved)
    
    def form_invalid(self, form):
        print("form invalid", form)
        return HttpResponse(form)
    
    '''
         
    

class RestaurantStockUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.RestaurantStock
    form_class = forms.RestaurantStockForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
    
class RestaurantStockDetailView(generic.DetailView):
    model = models.RestaurantStock
    form_class = forms.RestaurantStockForm
    template_name = "restaurants/restaurantstock_detail.html"


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
