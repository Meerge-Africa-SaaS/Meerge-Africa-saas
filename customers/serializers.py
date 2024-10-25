from rest_framework import serializers

from . import models


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            "id",
            "customer",
            "restaurant",
            "menu_item",
            "add_on",            
            "delivery_address",
            "driver_note",
            "created",
            "last_updated",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "alt_phone_number",
            "address",
            'allergies',
            "first_time_food_tryouts",
            "healthy_diet_goals",
            "city",
        ]
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": False},
            "phone_number": {"required": False},
            "alt_phone_number": {"required": False},
            "address": {"required": False},
            "allergies": {"required": False},
            "first_time_food_tryouts": {"required": False},
            "healthy_diet_goals": {"required": False},
            "city": {"required": False},
        }
