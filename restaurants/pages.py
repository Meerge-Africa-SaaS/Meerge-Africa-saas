from typing import Any

from django.urls import path
from django.views import generic

from restaurants.models import Restaurant

app_name = "restaurants"


class DashboardView(generic.DetailView):
    model = Restaurant
    slug_field = "slug"
    slug_url_kwarg = "restaurant"
    context_object_name = "restaurant"
    template_name = "restaurants/pages/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["empty"] = "empty" in self.request.GET
        return context


class SettingsView(generic.DetailView):
    model = Restaurant
    slug_field = "slug"
    slug_url_kwarg = "restaurant"
    context_object_name = "restaurant"
    template_name = "restaurants/pages/settings.html"


urlpatterns = (
    path("", DashboardView.as_view(), name="dashboard"),
    path("/settings", SettingsView.as_view(), name="settings"),
)
