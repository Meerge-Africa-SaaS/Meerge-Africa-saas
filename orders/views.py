from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DeliveryAgent
from .serializers import DeliveryAgentSerializer


from django.dispatch import receiver
''' 
@receiver(delivery_request_created)
def handle_delivery_request_created(sender, instance, created, kwargs):
    if created:
        print("\n"*10, instance, "\n"*10)
 '''


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

class DeliveryAgentUpdateProfileViewApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        try:
            delivery_agent = DeliveryAgent.objects.get(owner=request.user)
        except DeliveryAgent.DoesNotExist:
            return Response({"error": "Delivery agent profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DeliveryAgentSerializer(delivery_agent, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)