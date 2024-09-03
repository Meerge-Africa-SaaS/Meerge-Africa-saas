from cities_light.models import City
from django import forms
from inventory.models import Category
from inventory.models import Supplier
from inventory.models import Item

from . import models

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
            "city",
        ]

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.all()


class SupplyManagerForm(forms.ModelForm):
    class Meta:
        model = models.SupplyManager
        fields = [
            "supplier",
        ]

    def __init__(self, *args, **kwargs):
        super(SupplyManagerForm, self).__init__(*args, **kwargs)
        self.fields["supplier"].queryset = Supplier.objects.all()
