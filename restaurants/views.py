import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


class RestaurantMixin:
    model = models.Restaurant
    context_object_name = "restaurant"


@require_http_methods(["GET"])
def existing_addons(request, restaurant: int):
    restaurant = get_object_or_404(models.Restaurant, pk=restaurant)
    addons = models.AddOn.objects.filter(restaurant=restaurant)
    return render(
        request, "restaurants/components/menu/existing-addons.html", {"addons": addons}
    )


@require_http_methods(["GET"])
def search_addons(request, restaurant: int):
    search = request.GET.get("q")
    restaurant = get_object_or_404(models.Restaurant, pk=restaurant)
    addons = models.AddOn.objects.filter(restaurant=restaurant, name__icontains=search)
    return render(
        request, "restaurants/components/menu/existing-addons.html", {"addons": addons}
    )


@require_http_methods(["POST"])
def select_addon(request, addon_id):
    addon = models.AddOn.objects.get(id=addon_id)
    return render(request, "restaurants/components/menu/selected-addon.html", {"addon": addon})


@require_http_methods(["POST"])
def remove_addon(request, addon_id):
    return HttpResponse("")

@require_http_methods(["POST"])
def create_addon(request, restaurant: int):
    restaurant = get_object_or_404(models.Restaurant, pk=restaurant)
    addon = models.AddOn.objects.create(
        restaurant=restaurant,
        name=request.POST.get("name"),
        price=request.POST.get("price"),
    )
    return render(request, "restaurants/components/menu/selected-addon.html", {"addon": addon})


@require_http_methods(["POST"])
def save_addons(request):
    selected_addons = request.POST.getlist("selected_addons[]")
    # Save the selected addons to your menu item
    # Return updated menu addons section
    return render(request, "menu-addons.html", {"selected_addons": selected_addons})
