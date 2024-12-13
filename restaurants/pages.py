from typing import Any

from django.shortcuts import redirect
from django.urls import path, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from restaurants import views
from core.models import User
from restaurants.models import Restaurant, RestaurantStore, RestaurantStock, Staff
from restaurants import forms
from restaurants.forms import AddOnForm, MenuItemForm
from django.templatetags.static import static

from inventory.models import Category as StockCategory

app_name = "restaurants"


@method_decorator(login_required, name="dispatch")
class RestaurantRedirectView(generic.TemplateView):
    template_name = "restaurants/pages/not-allowed.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, Staff):
            return redirect(
                reverse("restaurants:dashboard", args=(user.restaurants.custom_link,))
            )
        elif hasattr(user, "staff"):
            return redirect(
                reverse("restaurants:dashboard", args=(user.staff.restaurants.custom_link,))
            )
        return super().get(request, *args, **kwargs)


class RestaurantMixin:
    model = Restaurant
    slug_field = "custom_link"
    slug_url_kwarg = "restaurant"
    context_object_name = "restaurant"


class DashboardView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["empty"] = "empty" in self.request.GET
        return context
    

class InventoryView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/inventory.html"
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        restaurant = self.object
        context["restaurant_stores"] = restaurant.stores.all()
        context["restaurant_store_form"] =forms.RestaurantStoreForm
        return context
    
    
class RestaurantStoreDetailView(RestaurantMixin, generic.DetailView):
    #model = RestaurantStore
    form_class = forms.RestaurantStoreForm
    template_name = "restaurants/pages/inventory/restaurantstore_detail.html"
    
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        print("kwargs\n"*10,kwargs, "\n"*10)
        print(self.kwargs.get("restaurantstore"))
        context = super().get_context_data(**kwargs)
        restaurant = self.object
        # Needed to do reverse like this, normal reverse is not working temporarily due to migration issues to reflect, will resolve and use reverse lookup for the query
        restaurant_store = RestaurantStore.objects.get(id = self.kwargs.get("restaurantstore"))
        context["restaurant_store"] = restaurant_store
        context["restaurant_stock_form"] =forms.RestaurantStockForm
        context["restaurant_stocks"] = restaurant_store.stocks.all()
        context["stock_categories"] = StockCategory.objects.all()
        
        print(context)
        return context
    

class SettingsView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/settings.html"


class ProfileView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/user-profile.html"


class BusinessView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/business-profile.html"

class MenuView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/menu.html"


    def get_add_menu_item_form(self):
        form_cls = MenuItemForm
        initial = {
            "restaurant": self.object,
        }
        return form_cls(initial=initial)
    
    def get_add_addon_form(self):
        form_cls = AddOnForm
        initial = {
            "restaurant": self.object,
        }
        return form_cls(initial=initial)
    

    def get_menu_items(self):
        # TODO: use actual menu items
        return [
            {
                "id": 1,
                "name": "Spaghetti",
                "price": 5000,
                "category": "Main Course",
                "status": "available",
                "ready_time": "1hr 24min",
                "image": static("images/food/spaghetti.png"),
            },
            {
                "id": 2,
                "name": "BBQ Pilled Pork Sandwich",
                "price": 5000,
                "category": "Main Course",
                "status": "available",
                "ready_time": "1hr 24min",
                "image": static("images/food/bbq-pulled-pork-sandwich.png")
            },
            {
                "id": 3,
                "name": "Avocado Toast",
                "price": 5000,
                "category": "Main Course",
                "status": "unlisted",
                "ready_time": "1hr 24min",
                "image": static("images/food/avocado-toast.png")
            },
            {
                "id": 4,
                "name": "Shrimp Fried Rice",
                "price": 5000,
                "category": "Main Course",
                "status": "available",
                "ready_time": "1hr 24min",
                "image": static("images/food/shrimp-fried-rice.png")
            },
            {
                "id": 5,
                "name": "Buffalo Chicken Wings",
                "price": 5000,
                "category": "Main Course",
                "status": "unlisted",
                "ready_time": "1hr 24min",
                "image": static("images/food/buffalo-chicken-wings.png")
            },
            {
                "id": 6,
                "name": "Margherita Pizza",
                "price": 5000,
                "category": "Main Course",
                "status": "available",
                "ready_time": "1hr 24min",
                "image": static("images/food/margherita-pizza.png")
            }
        ]
    
    def get_addons(self):
        return [
            {
                "id": 1,
                "name": "Extra Cheese",
                "price": 500,
                "status": "available",
            },
            {
                "id": 2,
                "name": "Extra Meat",
                "price": 500,
                "status": "available",
            },
            {
                "id": 3,
                "name": "Extra Sauce",
                "price": 500,
                "status": "available",
            },
            {
                "id": 4,
                "name": "Extra Veggies",
                "price": 500,
                "status": "available",
            },
            {
                "id": 5,
                "name": "Extra Toppings",
                "price": 500,
                "status": "available",
            },
        ]
    
    def get_drinks(self):
        return [
            {
                "id": 1,
                "name": "Coke",
                "price": 500,
                "status": "available",
            },
            {
                "id": 2,
                "name": "Fanta",
                "price": 500,
                "status": "available",
            },
            {
                "id": 3,
                "name": "Sprite",
                "price": 500,
                "status": "available",
            },
            {
                "id": 4,
                "name": "Pepsi",
                "price": 500,
                "status": "available",
            },
            {
                "id": 5,
                "name": "Mirinda",
                "price": 500,
                "status": "available",
            },
        ]
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["menu_items"] = self.get_menu_items()
        context["addons"] = self.get_addons()
        context["drinks"] = self.get_drinks()
        context["add_menu_item_form"] = self.get_add_menu_item_form()
        context["add_addon_form"] = self.get_add_addon_form()

        return context



urlpatterns = (
    path("", DashboardView.as_view(), name="dashboard"),
    path("inventory/", InventoryView.as_view(), name="inventory"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("profile/", ProfileView.as_view(), name="user_profile"),
    path("business/", BusinessView.as_view(), name="business_profile"),
    path("menu/", MenuView.as_view(), name="menu"),
)
