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
