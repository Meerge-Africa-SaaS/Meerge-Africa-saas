from typing import Any

from django.shortcuts import redirect
from django.urls import path, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from core.models import User
from restaurants.models import Restaurant, Staff

app_name = "restaurants"


@method_decorator(login_required, name="dispatch")
class RestaurantRedirectView(generic.TemplateView):
    template_name = "restaurants/pages/no-allowed.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, Staff):
            return redirect(
                reverse("restaurants:dashboard", args=(user.restaurants.id,))
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
