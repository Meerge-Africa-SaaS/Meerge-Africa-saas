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
            'phone_number', 
            'alternative_phone_number', 
            'email', 
            'available_work_days_hours'
        ]
