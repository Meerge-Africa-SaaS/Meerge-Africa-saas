import string

from cities_light.models import City
from django import forms
from phonenumber_field.formfields import PhoneNumberField

from inventory.models import Category, Item, Supplier

from . import models

from django.contrib.auth import get_user_model

USER = get_user_model()

SUPPLIER_CATEGORIES = [
    ("Fruits & Nuts", "Fruits & Nuts"),
    ("Grain Products", "Grain Products"),
    ("Spices & Seasoning", "Spices & Seasoning"),
    ("Baking Products", "Baking Products"),
    ("Drinks & Beverages", "Drinks & Beverages"),
    ("Seafood", "Seafood"),
    ("Spread & Sweeteners", "Spread & Sweeteners"),
    ("Vegetables", "Vegetables"),
    ("Meat & Poultry", "Meat & Poultry"),
    ("Oil & Fats", "Oil & Fats"),
    ("Dairy Products", "Dairy Products"),
    ("Frozen Foods", "Frozen Foods"),
    ("Canned Foods", "Canned Foods"),
    ("Soups & Condiments", "Soups & Condiments"),
    ("Snacks & Sweets", "Snacks & Sweets"),
    ("Others", "Others"),
]

LABELS = {
    "first_name": "First Name",
    "last_name": "Last Name",
    "phone_number": "Phone Number",
    "email": "Email Address",
    "password": "Password",
    "name": "Registered Business Name",
    "business_phone_number": "Business Phone Number",
    "business_email": "Business Email Address",
    "business_address": "Business Address",
    "supplier_category": "Supplier Category",
    "bank_name": "Bank Name",
    "account_number": "Account Number",
    "account_name": "Account Name",
    "business_registration_number": "CAC Registration Number",
    "business_document": "Business Document",
    "premises_license": "Food business premises license",
}


def add_placeholder(field: str, form: forms.Form) -> None:
    form.fields[field].widget.attrs["placeholder"] = LABELS[field]


class SupplierBasicInfoForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    phone_number = PhoneNumberField(
        label="Phone Number",
        region="NG",
    )
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(SupplierBasicInfoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            add_placeholder(field, self)

    def clean_password(self) -> str:
        errors: list[str] = []
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        if len(password) > 64:
            errors.append("Password must be no more than 64 characters")
        if not any(char.isdigit() for char in password):
            errors.append("Password must contain at least one digit")
        if not any(char.isupper() for char in password):
            errors.append("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            errors.append("Password must contain at least one lowercase letter")
        if not any(char in string.punctuation for char in password):
            errors.append(
                "Password must contain at least one special character"
            )
        if errors:
            raise forms.ValidationError(errors)
        return password


class SupplierBusinessInfoForm(forms.Form):
    # business info
    name = forms.CharField(max_length=100, label="Registered Business Name")
    business_phone_number = PhoneNumberField(
        label="Business Phone Number",
    )
    business_email = forms.EmailField(label="Business Email Address")
    business_address = forms.CharField(max_length=100, label="Business Address")

    # supplier info
    supplier_category = forms.MultipleChoiceField(
        choices=SUPPLIER_CATEGORIES, label="Supplier Category"
    )

    # business account details
    bank_name = forms.CharField(max_length=100, label="Bank Name")
    account_number = forms.CharField(max_length=100, label="Account Number")
    account_name = forms.CharField(max_length=100, label="Account Name")

    # legal documents
    business_registration_number = forms.CharField(
        max_length=100, label="CAC Registration Number"
    )
    business_document = forms.FileField(label="Business Document")
    premises_license = forms.FileField(
        label="Food business premises license", required=False
    )

    def __init__(self, *args, **kwargs):
        super(SupplierBusinessInfoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            add_placeholder(field, self)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = [
            "name",
        ]


class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = [
            "unit_of_measure",
            "name",
            "price",
            "expiry_date",
            "category",
            "supplier",
        ]

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
        self.fields["supplier"].queryset = Supplier.objects.all()


class StockForm(forms.ModelForm):
    class Meta:
        model = models.Stock
        fields = [
            "quantity",
            "item",
        ]

    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields["item"].queryset = Item.objects.all()


class SupplierForm(forms.ModelForm):
    class Meta:
        model = models.Supplier
        fields = [
            "name",
            "owner",
            "city",
            "email",
            "phone_number",
            "cac_reg_number",
            "cac_certificate",
            "business_license",
            "category",
            "profile_img",
            "cover_img",
            "address",
        ]

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.all()
        self.fields["owner"].queryset = User.objects.all()
        

class ViewSupplierForm(forms.ModelForm):
    class Meta:
        model = models.Supplier
        fields = [
            "name",
            "owner",
            "city",
            "email",
            "phone_number",
            "category",
            "profile_img",
            "cover_img",
            "address"
        ]

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.all()


class SupplyManagerSignupForm(forms.ModelForm):
    class Meta:
        model = models.SupplyManager
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "supply_business",
        ]

    def __init__(self, *args, **kwargs):
        super(SupplyManagerForm, self).__init__(*args, **kwargs)
        self.fields["supply_business"].queryset = Supplier.objects.all()


class SupplyManagerForm(forms.ModelForm):
    class Meta:
        model = models.SupplyManager
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "supply_business",
        ]

    def __init__(self, *args, **kwargs):
        super(SupplyManagerForm, self).__init__(*args, **kwargs)
        self.fields["supply_business"].queryset = Supplier.objects.all()
