from rest_framework import viewsets, permissions

from . import serializers
from . import models


class DeliveryAgentViewSet(viewsets.ModelViewSet):
    """ViewSet for the DeliveryAgent class"""

    queryset = models.DeliveryAgent.objects.all()
    serializer_class = serializers.DeliveryAgentSerializer
    permission_classes = [permissions.IsAuthenticated]
