import os

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from formtools.wizard.views import SessionWizardView

from config.form_fields import PhoneNumberField
from restaurants.models import Restaurant
from phonenumber_field.phonenumber import PhoneNumber
from django_htmx.http import HttpResponseClientRedirect

# from world.models import City

BUSINESS_CATEGORY_CHOICES = [
    ("cafe", "Cafe"),
    ("hotel", "Hotel"),
    ("lounge", "Lounge"),
    ("food-joint", "Food Joint"),
    ("street-vendor", "Street Vendor"),
]

PLACEHOLDERS = {
    "first_name": "First Name",
    "last_name": "Last Name",
    "phone_number": "Enter Your Phone Number",
    "email": "Email Address",
    "password": "Create your password",
    "name": "Registered Business Name",
    "business_phone_number": "Business Phone Number",
    "business_email": "Business Email Address",
    "business_address": "Business Address",
    "business_category": "Business Category",
    "bank_name": "Bank Name",
    "account_number": "Account Number",
    "account_name": "Account Name",
    "business_registration_status": "Business Registration Status",
    "business_registration_number": "CAC Registration Number",
    "business_document": "Business Document",
    "premises_license": "Food business premises license",
}


def show_cac_field_condition(wizard: SessionWizardView):
    """Condition to show the CAC field"""
    cleaned_data = wizard.get_cleaned_data_for_step("step1") or {}
    return cleaned_data.get("business_registration_status") == "registered"


def add_placeholder(field: str, form: forms.Form) -> None:
    form.fields[field].widget.attrs["placeholder"] = PLACEHOLDERS[field]


class OnboardingForm1(forms.Form):
    """The first form for restaurant staff onboarding."""

    name = forms.CharField(max_length=100, label="Registered Business Name")
    business_phone_number = PhoneNumberField(
        label="Business Phone Number",
    )
    business_email = forms.EmailField(label="Business Email Address")
    business_address = forms.CharField(max_length=100, label="Business Address")

    business_category = forms.ChoiceField(
        choices=BUSINESS_CATEGORY_CHOICES, label="Food Business Type"
    )

    business_registration_status = forms.ChoiceField(
        choices=[
            ("registered", "Registered"),
            ("unregistered", "Unregistered"),
        ],
        label="Business Registration Status",
    )

    def __init__(self, *args, **kwargs):
        super(OnboardingForm1, self).__init__(*args, **kwargs)
        for field in self.fields:
            add_placeholder(field, self)

    def clean_business_phone_number(self) -> PhoneNumber:
        phone_number: PhoneNumber = self.cleaned_data["business_phone_number"]
        if Restaurant.objects.filter(
            phone_number=phone_number.as_e164.replace(" ", "")
        ).exists():
            raise forms.ValidationError(
                "Restaurant with this phone number already exists."
            )
        return phone_number

    def clean_business_email(self):
        email = self.cleaned_data["business_email"]
        if Restaurant.objects.filter(email=email).exists():
            raise forms.ValidationError("Restaurant with this email already exists.")
        return email

    def clean_name(self):
        name = self.cleaned_data["name"]
        # do case-insensitive check
        if Restaurant.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Restaurant with this name already exists.")
        return name


class OnboardingForm2A(forms.Form):
    """The second form for restaurant staff onboarding."""

    # legal documents
    business_registration_number = forms.CharField(
        max_length=100, label="CAC Registration Number"
    )
    business_document = forms.FileField(label="CAC Document", required=True)
    premises_license = forms.FileField(
        label="Food business premises license", required=False
    )

    def __init__(self, *args, **kwargs):
        super(OnboardingForm2A, self).__init__(*args, **kwargs)
        for field in self.fields:
            add_placeholder(field, self)


class OnboardingForm2B(forms.Form):
    """The second form for restaurant staff onboarding."""

    # legal documents
    premises_license = forms.FileField(
        label="Food business premises license", required=False
    )

    def __init__(self, *args, **kwargs):
        super(OnboardingForm2B, self).__init__(*args, **kwargs)
        for field in self.fields:
            add_placeholder(field, self)


class OnboardingWizardView(SessionWizardView):
    form_list = [
        ("step1", OnboardingForm1),
        ("step2A", OnboardingForm2A),
        ("step2B", OnboardingForm2B),
    ]
    templates = {
        "step1": "restaurants/onboarding/wizard/step-1.html",
        "step2A": "restaurants/onboarding/wizard/step-2a.html",
        "step2B": "restaurants/onboarding/wizard/step-2b.html",
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
                }
            )
        return initial

    def done(self, form_list, **kwargs):
        user = self.request.user
        form1, form2 = form_list
        name = form1.cleaned_data["name"]
        phone_number = form1.cleaned_data["business_phone_number"]
        email = form1.cleaned_data["business_email"]
        address = form1.cleaned_data["business_address"]
        # create a restaurant
        restaurant = Restaurant.objects.create(
            name=name,
            phone_number=phone_number,
            email=email,
            city=None,
            country=None,
            address=address,
        )
        restaurant.owner.add(user)
        restaurant.save()
        messages.success(
            self.request, f"Your restaurant {restaurant.name} has been created"
        )
        return HttpResponseClientRedirect(
            reverse("restaurants:dashboard", args=(restaurant.custom_link,))
        )


class OnboardingView(generic.TemplateView):
    template_name = "restaurants/onboarding/onboarding.html"
