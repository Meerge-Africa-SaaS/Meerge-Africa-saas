from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms


class DeliveryAgentListView(generic.ListView):
    model = models.DeliveryAgent
    form_class = forms.DeliveryAgentForm


class DeliveryAgentCreateView(generic.CreateView):
    model = models.DeliveryAgent
    form_class = forms.DeliveryAgentForm


class DeliveryAgentDetailView(generic.DetailView):
    model = models.DeliveryAgent
    form_class = forms.DeliveryAgentForm


class DeliveryAgentUpdateView(generic.UpdateView):
    model = models.DeliveryAgent
    form_class = forms.DeliveryAgentForm
    pk_url_kwarg = "pk"


class DeliveryAgentDeleteView(generic.DeleteView):
    model = models.DeliveryAgent
    success_url = reverse_lazy("orders_DeliveryAgent_list")
