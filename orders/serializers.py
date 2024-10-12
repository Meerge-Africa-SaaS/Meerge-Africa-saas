from rest_framework import serializers

from . import models



class DeliveryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeliveryRequest
        fields = [
            "id",
            "order",
            "status",
            "deliveryagent",
            "created",
            "last_updated",
        ]

class DeliveryAgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DeliveryAgent
        fields = [
            "created",
            "last_updated",
        ]
