from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import HttpResponse

from django.template import Template, RequestContext
from django.template.response import TemplateResponse

from . import models
from . import forms


class HTMXDeliveryAgentListView(generic.ListView):
    model = models.DeliveryAgent
    form_class = forms.DeliveryAgentForm

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = {
            "model_id": self.model._meta.verbose_name_raw,
            "objects": self.get_queryset(),
        }
        return TemplateResponse(request, "htmx/list.html", context)


class HTMXDeliveryAgentCreateView(generic.CreateView):
    model = models.DeliveryAgent
    form_class = forms.DeliveryAgentForm

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


class HTMXDeliveryAgentDeleteView(generic.DeleteView):
    model = models.DeliveryAgent
    success_url = reverse_lazy("orders_DeliveryAgent_htmx_list")

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse()
