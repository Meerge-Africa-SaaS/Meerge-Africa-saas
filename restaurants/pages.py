from typing import Any

from django.urls import path
from django.views import generic

from restaurants.models import Restaurant

app_name = "restaurants"


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


class SettingsView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/settings.html"


class ProfileView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/user-profile.html"


class BusinessView(RestaurantMixin, generic.DetailView):
    template_name = "restaurants/pages/business-profile.html"


urlpatterns = (
    path("", DashboardView.as_view(), name="dashboard"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("profile/", ProfileView.as_view(), name="user_profile"),
    path("business/", BusinessView.as_view(), name="business_profile"),
)
