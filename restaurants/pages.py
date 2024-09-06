from typing import Any

from django.urls import path
from django.views import generic

app_name = "restaurants"


class DashboardView(generic.TemplateView):
    template_name = "restaurants/pages/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["empty"] = "empty" in self.request.GET
        return context


class SettingsView(generic.TemplateView):
    template_name = "restaurants/pages/settings.html"


urlpatterns = (
    path("", DashboardView.as_view(), name="dashboard"),
    path("settings/", SettingsView.as_view(), name="settings"),
)
