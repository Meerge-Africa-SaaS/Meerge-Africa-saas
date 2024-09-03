from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import HttpResponse

from django.template import Template, RequestContext
from django.template.response import TemplateResponse

from . import models
from . import forms


class HTMXCategoryListView(generic.ListView):
    model = models.Category
    form_class = forms.CategoryForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXCategoryCreateView(generic.CreateView):
    model = models.Category
    form_class = forms.CategoryForm

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


class HTMXCategoryDeleteView(generic.DeleteView):
    model = models.Category
    success_url = reverse_lazy("inventory_Category_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()


class HTMXItemListView(generic.ListView):
    model = models.Item
    form_class = forms.ItemForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXItemCreateView(generic.CreateView):
    model = models.Item
    form_class = forms.ItemForm

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


class HTMXItemDeleteView(generic.DeleteView):
    model = models.Item
    success_url = reverse_lazy("inventory_Item_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()


class HTMXStockListView(generic.ListView):
    model = models.Stock
    form_class = forms.StockForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXStockCreateView(generic.CreateView):
    model = models.Stock
    form_class = forms.StockForm

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


class HTMXStockDeleteView(generic.DeleteView):
    model = models.Stock
    success_url = reverse_lazy("inventory_Stock_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()


class HTMXSupplierListView(generic.ListView):
    model = models.Supplier
    form_class = forms.SupplierForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXSupplierCreateView(generic.CreateView):
    model = models.Supplier
    form_class = forms.SupplierForm

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


class HTMXSupplierDeleteView(generic.DeleteView):
    model = models.Supplier
    success_url = reverse_lazy("inventory_Supplier_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()


class HTMXSupplyManagerListView(generic.ListView):
    model = models.SupplyManager
    form_class = forms.SupplyManagerForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXSupplyManagerCreateView(generic.CreateView):
    model = models.SupplyManager
    form_class = forms.SupplyManagerForm

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


class HTMXSupplyManagerDeleteView(generic.DeleteView):
    model = models.SupplyManager
    success_url = reverse_lazy("inventory_SupplyManager_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()
