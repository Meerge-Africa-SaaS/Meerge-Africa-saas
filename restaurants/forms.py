from django import forms
from phonenumber_field.formfields import PhoneNumberField

# from world.models import City
from core.models import User
from restaurants.models import Menu, MenuItem, Restaurant

from . import models

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


def add_placeholder(field: str, form: forms.Form) -> None:
    form.fields[field].widget.attrs["placeholder"] = PLACEHOLDERS[field]


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
        ]
        field_classes = {
            "phone_number": PhoneNumberField,
        }
        widgets = {
            "password": forms.PasswordInput(
                attrs={
                    "autocomplete": "new-password",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            add_placeholder(field, self)


class OnboardingForm1(forms.Form):
    """The first form for restaurant staff onboarding."""

    name = forms.CharField(max_length=100, label="Registered Business Name")
    business_phone_number = PhoneNumberField(
        label="Business Phone Number",
    )
    business_email = forms.EmailField(label="Business Email Address")
    business_address = forms.CharField(max_length=100, label="Business Address")

    business_category = forms.ChoiceField(
        choices=BUSINESS_CATEGORY_CHOICES, label="Supplier Category"
    )

    # business account details
    bank_name = forms.CharField(max_length=100, label="Bank Name")
    account_number = forms.CharField(max_length=100, label="Account Number")
    account_name = forms.CharField(max_length=100, label="Account Name")

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


class OnboardingForm2A(forms.Form):
    """The second form for restaurant staff onboarding."""

    # legal documents
    business_registration_number = forms.CharField(
        max_length=100, label="CAC Registration Number"
    )
    business_document = forms.FileField(label="Business Document")
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


class IngredientForm(forms.ModelForm):
    class Meta:
        model = models.Ingredient
        fields = [
            "name",
            "menu_item",
        ]

    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        self.fields["menu_item"].queryset = MenuItem.objects.all()


class MenuForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = [
            "date_from",
            "name",
            "date_to",
        ]


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = models.MenuItem
        fields = [
            "name",
            "price",
            "menu",
        ]

    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        self.fields["menu"].queryset = Menu.objects.all()


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = [
            "address",
            "name",
            "city",
            "country",
            "owner",
        ]

    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        # self.fields["city"].queryset = City.objects.all()
        self.fields["owner"].queryset = User.objects.all()


class ChefForm(forms.ModelForm):
    class Meta:
        model = models.Chef
        fields = [
            "restaurants",
        ]

    def __init__(self, *args, **kwargs):
        super(ChefForm, self).__init__(*args, **kwargs)
        self.fields["restaurants"].queryset = Restaurant.objects.all()


class StaffForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = [
            "restaurants",
        ]

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields["restaurants"].queryset = Restaurant.objects.all()
