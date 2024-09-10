import os

from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django_htmx.http import HttpResponseClientRedirect
from formtools.wizard.views import SessionWizardView
from more_itertools import first
from django_htmx.http import HttpResponseClientRedirect

from . import forms, models


class SignupView(generic.CreateView):
    form_class = forms.SignupForm
    success_url = reverse_lazy("core_User_signin")
    template_name = "registration/restaurant/signup.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(
            self.request,
            "Your account has been created successfully. Please login to continue",
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return super().get_success_url() + "?next=" + reverse("restaurant_onboarding")


class EmailVerificationView(generic.TemplateView):
    template_name = "registration/restaurant/email_verification.html"


def show_cac_field_condition(wizard: SessionWizardView):
    """Condition to show the CAC field"""
    cleaned_data = wizard.get_cleaned_data_for_step("step1") or {}
    return cleaned_data.get("business_registration_status") == "registered"


class OnboardingWizardView(SessionWizardView):
    form_list = [
        ("step1", forms.OnboardingForm1),
        ("step2A", forms.OnboardingForm2A),
        ("step2B", forms.OnboardingForm2B),
    ]
    templates = {
        "step1": "registration/restaurant/onboarding_step1.html",
        "step2A": "registration/restaurant/onboarding_step2A.html",
        "step2B": "registration/restaurant/onboarding_step2B.html",
    }
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "temp"))
    condition_dict = {
        "step2A": show_cac_field_condition,
        "step2B": lambda wizard: not show_cac_field_condition(wizard),
    }

    def get_template_names(self) -> list[str]:
        return [self.templates[self.steps.current]]

    def get(self, request, *args, **kwargs):
        return self.render(self.get_form())

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == "step1":
            initial.update(
                {
                    "business_email": self.request.user.email,
                    "business_phone_number": str(self.request.user.phone_number).lstrip(
                        "+234"
                    ),
                    "account_name": self.request.user.get_full_name(),
                }
            )
        return initial

    def done(self, form_list, **kwargs):
        user = self.request.user
        # create a restaurant
        restaurant = models.Restaurant.objects.create(
            name=form_list[0].cleaned_data["name"],
            city=None,
            country=None,
            address=form_list[0].cleaned_data["business_address"],
        )
        restaurant.owner.add(user)
        restaurant.save()
        # create a staff account
        messages.success(
            self.request,
            "Your restaurant has been created successfully.",
        )
        return HttpResponseClientRedirect(
            reverse("restaurants:dashboard", args=[restaurant.slug])
        )


class OnboardingView(generic.TemplateView):
    template_name = "registration/restaurant/onboarding.html"


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


class MenuListView(generic.ListView):
    model = models.Menu
    form_class = forms.MenuForm


class MenuCreateView(generic.CreateView):
    model = models.Menu
    form_class = forms.MenuForm


class MenuDetailView(generic.DetailView):
    model = models.Menu
    form_class = forms.MenuForm


class MenuUpdateView(generic.UpdateView):
    model = models.Menu
    form_class = forms.MenuForm
    pk_url_kwarg = "pk"


class MenuDeleteView(generic.DeleteView):
    model = models.Menu
    success_url = reverse_lazy("restaurant_Menu_list")


class MenuItemListView(generic.ListView):
    model = models.MenuItem
    form_class = forms.MenuItemForm


class MenuItemCreateView(generic.CreateView):
    model = models.MenuItem
    form_class = forms.MenuItemForm


class MenuItemDetailView(generic.DetailView):
    model = models.MenuItem
    form_class = forms.MenuItemForm


class MenuItemUpdateView(generic.UpdateView):
    model = models.MenuItem
    form_class = forms.MenuItemForm
    pk_url_kwarg = "pk"


class MenuItemDeleteView(generic.DeleteView):
    model = models.MenuItem
    success_url = reverse_lazy("restaurant_MenuItem_list")


class RestaurantListView(generic.ListView):
    model = models.Restaurant
    form_class = forms.RestaurantForm


class RestaurantCreateView(generic.CreateView):
    model = models.Restaurant
    form_class = forms.RestaurantForm


class RestaurantDetailView(generic.DetailView):
    model = models.Restaurant
    form_class = forms.RestaurantForm


class RestaurantUpdateView(generic.UpdateView):
    model = models.Restaurant
    form_class = forms.RestaurantForm
    pk_url_kwarg = "pk"


class RestaurantDeleteView(generic.DeleteView):
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
