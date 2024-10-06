from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = [
            "created",
            "name",
            "last_updated",
        ]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = [
            "last_updated",
            "unit_of_measure",
            "name",
            "id",
            "price",
            "created",
            "expiry_date",
            "category",
            "supplier",
        ]


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = [
            "quantity",
            "last_updated",
            "id",
            "created",
            "item",
        ]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supplier
        fields = [
            "id",
            "created",
            "name",
            "owner",
            "last_updated",
            "city",
            "email",
            "phone_number",
            "cac_reg_number",
            "cac_certificate",
            "business_license",
            "category",
            "profile_img",
            "cover_img",
            "address",
        ]


class SupplyManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SupplyManager
        fields = [
            "last_updated",
            "created",
            "supplier",
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "supply_business",
        ]
