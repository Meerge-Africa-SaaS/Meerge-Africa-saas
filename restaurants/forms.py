import os

from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from config.form_fields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from allauth.account.utils import setup_user_email
from allauth.account.models import EmailAddress

# from world.models import City
from core.models import User
from restaurants.models import (
    Menu,
    MenuCategory,
    MenuItem,
    Restaurant,
    RestaurantCategory,
    Staff,
    StaffInvitation,
)

from . import models


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


class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = models.MenuCategory
        fields = ["name", "description", "date_from", "date_to"]


class MenuForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = ["date_from", "name", "date_to", "category", "restaurant"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("user", None)
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"].queryset = Restaurant.objects.filter(owner=self.user)
        self.fields["category"].queryset = RestaurantCategory.objects.all()


class ViewMenuForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = ["date_from", "name", "date_to", "category", "restaurant"]

    def __init__(self, *args, **kwargs):
        super(ViewMenuForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["restaurant"].queryset = Restaurant.objects.filter(
                id=self.instance.restaurant.id
            )
            self.fields["category"].queryset = MenuCategory.objects.filter(
                category_ID=self.instance.category.category_ID
            )
        else:
            self.fields["restaurant"].queryset = Restaurant.objects.none()
            self.fields["category"].queryset = MenuCategory.objects.none()


class AddOnForm(forms.ModelForm):
    class Meta:
        model = models.AddOn
        fields = [
            "restaurant",
            "name",
            "price",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(AddOnForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"] = Restaurant.objects.filter(owner=self.user)

    def clean_name(self):
        name = self.cleaned_data("name")
        if not isinstance(name, str):
            raise forms.ValidationError("Value input must be alphabet only.")
        return name

    def clean_price(self):
        price = self.cleaned_data("price")
        if not price:
            price = 0
        if price and price < 0:
            raise forms.ValidationError("Price cannot be less than zero.")
        return price


class ViewAddOnForm(forms.ModelForm):
    class Meta:
        model = models.AddOn
        fields = ["restaurant", "name", "price"]

    def __init__(self, *args, **kwargs):
        super(ViewAddOnForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"] = Restaurant.objects.filter(add_ons=self.instance.pk)


class MenuItemForm(forms.ModelForm):
    # Adding the password field
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        help_text="Enter your password to confirm this action",
    )

    class Meta:
        model = models.MenuItem
        fields = [
            "menu",
            "restaurant",
            "name",
            "price",
            "portion",
            "size",
            "ingredient_details",
            "diet_type",
            "spice_level",
            "status",
            "nutritional_info_summary",
            "add_ons",
            "ready_in",
            "discount_percentage",
            "image",
            "video",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(MenuItemForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"].queryset = Restaurant.objects.filter(owner=self.user)

    def clean_restaurant(self):
        restaurant = self.cleaned_data("restaurant")
        if restaurant.owner != self.user:
            raise forms.ValidationError("You do not own this restaurant")
        return restaurant

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.user.check_password(password):
            raise forms.ValidationError("Incorrect Password")
        return password

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise forms.ValidationError("Forms cannot be negative")

    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data.get("discount_percentage")
        if discount_percentage < 0:
            raise forms.ValidationError("Discount Percentage cannot be negative")
        return discount_percentage


class OwnerViewMenuItemForm(forms.ModelForm):
    class Meta:
        model = models.MenuItem
        fields = [
            "name",
            "price",
            "menu",
            "restaurant",
            "portion",
            "size",
            "status",
            "ready_in",
            "add_ons",
            "ingredient_details",
            "image",
            "video",
            "diet_type",
            "spice_level",
            "nutritional_info_summary",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(OwnerViewMenuItemForm, self).__init__(*args, **kwargs)
        self.fields["restaurant"].queryset = Restaurant.objects.filter(owner=self.user)
        if "restaurant" in self.fields:
            restaurant = self.fields["restaurant"]
        self.fields["menu"].queryset = Menu.objects.filter(restaurant=restaurant)

    def clean_restaurant(self):
        restaurant = self.cleaned_data("restaurants")
        if restaurant.owner != self.user:
            raise forms.ValidationError("You do not own this restaurant")
        return restaurant


class GeneralViewMenuItemForm(forms.ModelForm):
    class Meta:
        model = models.MenuItem
        fields = [
            "name",
            "price",
            "menu",
            "restaurant",
            "portion",
            "size",
            "status",
            "ready_in",
            "add_ons",
            "ingredient_details",
            "image",
            "video",
            "diet_type",
            "spice_level",
            "nutritional_info_summary",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(GeneralViewMenuItemForm, self).__init__(*args, **kwargs)
        if "restaurant" in self.fields:
            restaurant = self.fields["restaurant"]
        self.fields["menu"].queryset = Menu.objects.filter(restaurant=restaurant)


class RestaurantCategoryForm(forms.ModelForm):
    class Meta:
        model = models.RestaurantCategory
        fields = ["name", "description"]


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = [
            "address",
            "name",
            "email",
            "phone_number",
            "business_category",
            "business_reg_details",
            "cac_reg_number",
            "cac_certificate",
            "business_license",
            "profile_img",
            "cover_img",
            "city",
            "country",
            "owner",
            "add_ons",
            "custom_link",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(RestaurantForm, self).__init__(*args, **kwargs)
        # self.fields["city"].queryset = City.objects.all()
        #
        if self.instance.pk:
            self.fields["owner"].queryset = Restaurant.objects.filter(owner=self.user)

        else:
            self.fields["owner"].queryset = User.objects.all()

    def clean_custom_link(self):
        custom_link = self.cleaned_data.get("custom_link")
        if not custom_link:
            return custom_link
        if not custom_link.isalnum():
            raise forms.ValidationError("Special characters are not allowed.")
        if custom_link and custom_link < 3:
            raise forms.ValidationError(
                "Custom link tagname cannot be less than 3 characters"
            )
        if custom_link > 24:
            raise forms.ValidationError(
                "Custom link tagname cannot be more than 24 characters"
            )

        return custom_link


class GeneralViewRestaurantForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = [
            "address",
            "name",
            "email",
            "phone_number",
            "business_category",
            "business_reg_details",
            "cac_reg_number",
            "cac_certificate",
            "business_license",
            "profile_img",
            "cover_img",
            "city",
            "country",
            "owner",
            "add_ons",
            "custom_link",
        ]

    def __init__(self, *args, **kwargs):
        super(GeneralViewRestaurantForm, self).__init__(*args, **kwargs)
        # self.fields["city"].queryset = City.objects.all()
        self.fields["owner"].queryset = User.objects.all()
        self.fields["restaurant"] = Restaurant.objects.all()

    def clean_custom_link(self):
        custom_link = self.cleaned_data.get("custom_link")
        if not custom_link:
            pass
        if not custom_link.isalnum():
            raise forms.ValidationError("Special characters are not allowed.")
        if custom_link and custom_link < 3:
            raise forms.ValidationError(
                "Custom link tagname cannot be less than 3 characters"
            )
        if custom_link > 24:
            raise forms.ValidationError(
                "Custom link tagname cannot be more than 24 characters"
            )

        return custom_link


class RestauarantStoreForm(forms.ModelForm):
    class Meta:
        model = models.RestaurantStore
        fields = ["restaurant", "name", "description", "image", "section_name"]


class RestauarantStockForm(forms.ModelForm):
    class Meta:
        model = models.RestaurantStock
        fields = [
            "category",
            "name",
            "image",
            "stock_type",
            "purchasing_price",
            "quantity",
            "measuring_unit",
            "restaurant",
        ]


""" 

class ChefForm(forms.ModelForm):
    class Meta:
        model = models.Chef
        fields = [
            "restaurants",
        ]

    def __init__(self, *args, **kwargs):
        super(ChefForm, self).__init__(*args, **kwargs)
        self.fields["restaurants"].queryset = Restaurant.objects.all()

 """


class StaffForm(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = [
            "restaurants",
        ]

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields["restaurants"].queryset = Restaurant.objects.all()


class RestaurantLogoForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = ["profile_img"]


class RestaurantCoverForm(forms.ModelForm):
    class Meta:
        model = models.Restaurant
        fields = ["cover_img"]


class RegistrationForm(SignupForm):
    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "Enter your first name"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "Enter your last name"}),
    )
    phone_number = PhoneNumberField(
        label="Phone Number",
    )

    def clean_phone_number(self) -> PhoneNumber:
        phone_number: PhoneNumber = self.cleaned_data["phone_number"]
        if User.objects.filter(
            phone_number=phone_number.as_e164.replace(" ", "")
        ).exists():
            raise forms.ValidationError("User with this phone number already exists.")
        return phone_number

    def clean(self):
        email = self.cleaned_data.get("email")
        if email:
            self.cleaned_data["username"] = email.split("@")[0]
        return super().clean()

    def save(self, request):
        request.session["verification_email"] = self.cleaned_data["email"]
        user = super().save(request)
        user.phone_number = self.cleaned_data["phone_number"]
        owner_grp, _ = Group.objects.get_or_create(name="Restaurant Owner")
        owner_sys_grp, _ = Group.objects.get_or_create(name="owner")
        user.groups.add(owner_grp)
        user.groups.add(owner_sys_grp)
        user.save()
        request.session["verification_email"] = user.email
        return user

    # def signup(self, request: HttpRequest, user: User) -> None:
    #     user.phone_number = self.cleaned_data["phone_number"]
    #     owner_grp, _ = Group.objects.get_or_create(name="Restaurant Owner")
    #     user.groups.add(owner_grp)
    #     user.save()
    #     request.session["verification_email"] = user.email
    #     return super().signup(request, user)


class InvitationRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "Enter your first name"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "Enter your last name"}),
    )
    phone_number = PhoneNumberField(label="Phone Number")
    invite_key = forms.CharField(widget=forms.HiddenInput)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
    )

    class Meta:
        model = Staff
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "password",
            "invite_key",
        ]

    def clean_phone_number(self) -> PhoneNumber:
        phone_number: PhoneNumber = self.cleaned_data["phone_number"]
        if User.objects.filter(
            phone_number=phone_number.as_e164.replace(" ", "")
        ).exists():
            raise forms.ValidationError("User with this phone number already exists.")
        return phone_number

    def clean(self):
        email = self.cleaned_data.get("email")
        if email:
            self.cleaned_data["username"] = email.split("@")[0]
        return super().clean()

    def save(self, request):
        invitation_key = self.cleaned_data["invite_key"]
        invitation = get_object_or_404(StaffInvitation, key=invitation_key)
        staff = Staff.objects.create(
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=invitation.email,
            username=invitation.email.split("@")[0],
            phone_number=self.cleaned_data["phone_number"],
            role=invitation.role,
            restaurants=invitation.restaurant,
        )
        staff.set_password(self.cleaned_data["password"])
        staff.save()
        sys_grp, _ = Group.objects.get_or_create(name="staff")
        grp, _ = Group.objects.get_or_create(name=invitation.role)
        staff.groups.add(sys_grp)
        staff.groups.add(grp)
        staff.save()
        invitation.delete()
        setup_user_email(request, staff, [EmailAddress(email=staff.email)])
        return staff
