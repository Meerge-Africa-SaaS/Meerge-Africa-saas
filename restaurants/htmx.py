from typing import Any

from django.forms.forms import BaseForm
from django.http import HttpRequest
from django.shortcuts import HttpResponse, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models


class HTMXIngredientListView(generic.ListView):
    model = models.Ingredient
    form_class = forms.IngredientForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXIngredientCreateView(generic.CreateView):
    model = models.Ingredient
    form_class = forms.IngredientForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(request, "htmx/form.html", context)

    def form_valid(self, form):
        super().form_valid(form)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "object": self.object,
            "form": form,
        }
        return TemplateResponse(self.request, "htmx/create.html", context)

    def form_invalid(self, form):
        super().form_invalid(form)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(self.request, "htmx/form.html", context)


class HTMXIngredientDeleteView(generic.DeleteView):
    model = models.Ingredient
    success_url = reverse_lazy("restaurant_Ingredient_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()


class HTMXMenuListView(generic.ListView):
    model = models.Menu
    form_class = forms.MenuForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXMenuCreateView(generic.CreateView):
    model = models.Menu
    form_class = forms.MenuForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(request, "htmx/form.html", context)

    def form_valid(self, form):
        super().form_valid(form)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "object": self.object,
            "form": form,
        }
        return TemplateResponse(self.request, "htmx/create.html", context)

    def form_invalid(self, form):
        super().form_invalid(form)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(self.request, "htmx/form.html", context)


class HTMXMenuDeleteView(generic.DeleteView):
    model = models.Menu
    success_url = reverse_lazy("restaurant_Menu_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()


class HTMXMenuItemListView(generic.ListView):
    model = models.MenuItem
    form_class = forms.MenuItemForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXMenuItemCreateView(generic.CreateView):
    model = models.MenuItem
    form_class = forms.MenuItemForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(request, "htmx/form.html", context)

    def form_valid(self, form):
        super().form_valid(form)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "object": self.object,
            "form": form,
        }
        return TemplateResponse(self.request, "htmx/create.html", context)

    def form_invalid(self, form):
        super().form_invalid(form)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(self.request, "htmx/form.html", context)


class HTMXMenuItemDeleteView(generic.DeleteView):
    model = models.MenuItem
    success_url = reverse_lazy("restaurant_MenuItem_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()


class HTMXRestaurantListView(generic.ListView):
    model = models.Restaurant
    form_class = forms.RestaurantForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXRestaurantCreateView(generic.CreateView):
    model = models.Restaurant
    form_class = forms.RestaurantForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(request, "htmx/form.html", context)

    def form_valid(self, form):
        super().form_valid(form)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "object": self.object,
            "form": form,
        }
        return TemplateResponse(self.request, "htmx/create.html", context)

    def form_invalid(self, form):
        super().form_invalid(form)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(self.request, "htmx/form.html", context)


class HTMXRestaurantDeleteView(generic.DeleteView):
    model = models.Restaurant
    success_url = reverse_lazy("restaurant_Restaurant_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()


""" 
class HTMXChefListView(generic.ListView):
    model = models.Chef
    form_class = forms.ChefForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXChefCreateView(generic.CreateView):
    model = models.Chef
    form_class = forms.ChefForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(request, "htmx/form.html", context)

    def form_valid(self, form):
        super().form_valid(form)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "object": self.object,
            "form": form,
        }
        return TemplateResponse(self.request, "htmx/create.html", context)

    def form_invalid(self, form):
        super().form_invalid(form)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(self.request, "htmx/form.html", context)


class HTMXChefDeleteView(generic.DeleteView):
    model = models.Chef
    success_url = reverse_lazy("restaurant_Chef_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()
 """


class HTMXStaffListView(generic.ListView):
    model = models.Staff
    form_class = forms.StaffForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXStaffCreateView(generic.CreateView):
    model = models.Staff
    form_class = forms.StaffForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(request, "htmx/form.html", context)

    def form_valid(self, form):
        super().form_valid(form)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "object": self.object,
            "form": form,
        }
        return TemplateResponse(self.request, "htmx/create.html", context)

    def form_invalid(self, form):
        super().form_invalid(form)
        context = {
            "create_url": self.model.get_htmx_create_url(),
            "form": self.get_form(),
        }
        return TemplateResponse(self.request, "htmx/form.html", context)


class HTMXStaffDeleteView(generic.DeleteView):
    model = models.Staff
    success_url = reverse_lazy("restaurant_Staff_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()


class HTMXRestaurantLogoView(generic.FormView, generic.DetailView):
    model = models.Restaurant
    form_class = forms.RestaurantLogoForm
    template_name = "restaurants/components/business-profile/logo.html"
    context_object_name = "restaurant"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["logo"] = (
            self.object.profile_img.url if self.object.profile_img else None
        )
        print(context)
        return context

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class HTMXRestaurantCoverView(generic.FormView, generic.DetailView):
    model = models.Restaurant
    form_class = forms.RestaurantCoverForm
    template_name = "restaurants/components/business-profile/cover.html"
    context_object_name = "restaurant"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["cover_image"] = (
            self.object.cover_img.url if self.object.cover_img else None
        )
        return context

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
