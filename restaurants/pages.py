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
        
        print(context)
        return context
    

class SettingsView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/settings.html"


class ProfileView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/user-profile.html"


class BusinessView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/business-profile.html"


urlpatterns = (
    path("", DashboardView.as_view(), name="dashboard"),
    path("inventory/", InventoryView.as_view(), name="inventory"),
    path("RestaurantStore/detail/<int:restaurantstore>/",RestaurantStoreDetailView.as_view(),name="restaurant_RestaurantStore_detail",),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("profile/", ProfileView.as_view(), name="user_profile"),
    path("business/", BusinessView.as_view(), name="business_profile"),
)
