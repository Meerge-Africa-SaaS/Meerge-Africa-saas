from rest_framework import serializers

from . import models


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = [
            "id",
            "delivery_address",
            "created",
            "last_updated",
        ]

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        fields = [
            "last_name",
            "last_updated",
            "created",
            "address",
            "first_name",
            "city",
        ]
