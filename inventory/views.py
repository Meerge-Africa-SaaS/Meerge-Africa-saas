from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms


class SupplierCreateView(generic.TemplateView):
    template_name = "inventory/supplier_registration/base.html"


class CategoryListView(generic.ListView):
    model = models.Category
    form_class = forms.CategoryForm


class CategoryCreateView(generic.CreateView):
    model = models.Category
    form_class = forms.CategoryForm


class CategoryDetailView(generic.DetailView):
    model = models.Category
    form_class = forms.CategoryForm


class CategoryUpdateView(generic.UpdateView):
    model = models.Category
    form_class = forms.CategoryForm
    pk_url_kwarg = "pk"


class CategoryDeleteView(generic.DeleteView):
    model = models.Category
    success_url = reverse_lazy("inventory_Category_list")


class ItemListView(generic.ListView):
    model = models.Item
    form_class = forms.ItemForm


class ItemCreateView(generic.CreateView):
    model = models.Item
    form_class = forms.ItemForm


class ItemDetailView(generic.DetailView):
    model = models.Item
    form_class = forms.ItemForm


class ItemUpdateView(generic.UpdateView):
    model = models.Item
    form_class = forms.ItemForm
    pk_url_kwarg = "pk"


class ItemDeleteView(generic.DeleteView):
    model = models.Item
    success_url = reverse_lazy("inventory_Item_list")


class StockListView(generic.ListView):
    model = models.Stock
    form_class = forms.StockForm


class StockCreateView(generic.CreateView):
    model = models.Stock
    form_class = forms.StockForm


class StockDetailView(generic.DetailView):
    model = models.Stock
    form_class = forms.StockForm


class StockUpdateView(generic.UpdateView):
    model = models.Stock
    form_class = forms.StockForm
    pk_url_kwarg = "pk"


class StockDeleteView(generic.DeleteView):
    model = models.Stock
    success_url = reverse_lazy("inventory_Stock_list")


class SupplierListView(generic.ListView):
    model = models.Supplier
    form_class = forms.SupplierForm


class SupplierDetailView(generic.DetailView):
    model = models.Supplier
    form_class = forms.SupplierForm


class SupplierUpdateView(generic.UpdateView):
    model = models.Supplier
    form_class = forms.SupplierForm
    pk_url_kwarg = "pk"


class SupplierDeleteView(generic.DeleteView):
    model = models.Supplier
    success_url = reverse_lazy("inventory_Supplier_list")


class SupplyManagerListView(generic.ListView):
    model = models.SupplyManager
    form_class = forms.SupplyManagerForm


class SupplyManagerCreateView(generic.CreateView):
    model = models.SupplyManager
    form_class = forms.SupplyManagerForm


class SupplyManagerDetailView(generic.DetailView):
    model = models.SupplyManager
    form_class = forms.SupplyManagerForm


class SupplyManagerUpdateView(generic.UpdateView):
    model = models.SupplyManager
    form_class = forms.SupplyManagerForm
    pk_url_kwarg = "pk"


class SupplyManagerDeleteView(generic.DeleteView):
    model = models.SupplyManager
    success_url = reverse_lazy("inventory_SupplyManager_list")
