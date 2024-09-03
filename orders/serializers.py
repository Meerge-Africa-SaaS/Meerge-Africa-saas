from rest_framework import serializers

from . import models


class DeliveryAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeliveryAgent
        fields = [
            "created",
            "last_updated",
        ]
