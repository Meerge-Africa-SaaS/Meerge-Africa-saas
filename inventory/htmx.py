import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import HttpResponse

from django.template import Template, RequestContext
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import generic
from formtools.wizard.views import SessionWizardView

from . import forms, models


class HtmxSupplierRegistrationWizardView(SessionWizardView):
    form_list = [
        ("basic_info", forms.SupplierBasicInfoForm),
        ("business_info", forms.SupplierBusinessInfoForm),
    ]
    templates = {
        "basic_info": "inventory/supplier_registration/basic_info.html",
        "business_info": "inventory/supplier_registration/business_info.html",
    }
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, "temp")
    )

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get(self, request, *args, **kwargs):
        return self.render(self.get_form())

    def done(self, form_list, form_dict, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)
        full_name = f"{form_data['first_name']} {form_data['last_name']}"
        return HttpResponse(f"Supplier {full_name} created successfully")


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

class HTMXAdminStockListView(generic.ListView):
   model = models.Stock
   template_name = "htmx/stock_admin_list.html"  

   def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

   def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }

        if request.htmx:  
            return TemplateResponse(request, "htmx/stock_admin_list.html", context)

        
        return TemplateResponse(request, self.template_name, context)


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
    form_class = forms.ViewSupplierForm

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
