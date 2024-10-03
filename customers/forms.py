from cities_light.models import City
from django import forms
from . import models


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = [
            "delivery_address",
        ]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = [
            "last_name",
            "address",
            "first_name",
            "city",
        ]

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.all()
