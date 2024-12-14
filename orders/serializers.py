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
            'email',
            'first_name',
            'last_name',
            'phone_number', 
            'account_details',
            'address',
            'face_capture',
            'work_shift',
            'vehicle_type',
            'vehicle_brand',
            'plate_number',
            'drivers_license_id',
            'voters_number',
            'nin_number',
            'N_O_N_full_name',
            'N_O_N_phone_number',
            'guarantor_first_name',
            'guarantor_last_name',
            'guarantor_phone_number',
            'guarantor_occupation',
        ]
        extra_kwargs = {
            'email': {"required": False},
            'first_name': {"required": False},
            'last_name': {"required": False},
            'phone_number': {"required": False}, 
            'account_details': {"required": False},
            'address': {"required": False},
            'face_capture': {"required": False},
            'work_shift': {"required": False},
            'vehicle_type': {"required": False},
            'vehicle_brand': {"required": False},
            'plate_number': {"required": False},
            'drivers_license_id': {"required": False},
            'voters_number': {"required": False},
            'nin_number': {"required": False},
            'N_O_N_full_name': {"required": False},
            'N_O_N_phone_number': {"required": False},
            'guarantor_first_name': {"required": False},
            'guarantor_last_name': {"required": False},
            'guarantor_phone_number': {"required": False},
            'guarantor_occupation': {"required": False},
        }

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = [
            "cart",
            "item",
            "product_quantity",
        ]

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = [
            "customer",
        ]

class AddItemToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = [
            "cart",
            "item",
            "customer",
            "product_quantity",
        ]   

class RemoveItemFromCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = [
            "cartItem",
            "item",
            "customer",
            "product_quantity",
        ]

