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
            "SKU_No",
            "Product_Name",
            "Product_Image",
            "Product_Category",
            "Manufacturer_Name",
            "Price",
            "Units_Available",
            "Size",
            "Weight",
            "Availability_Status",
            "Discount_Percentage",
            "Delivery_Time_Estimate",
            "Pickup_Option",
            "Password",
        ]

class AdminViewAllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = [
            "id",
            "Product_Name",
            "Product_Image",
            "Product_Category",
            "Price",
            "Units_Available",
            "Size",
            "Discount_Percentage",
            "Availability_Status",
        ]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supplier
        fields = [
            "id",
            "created",
            "name",
            "last_updated",
            "city",
        ]


class SupplyManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SupplyManager
        fields = [
            "last_updated",
            "created",
            "supplier",
        ]
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = ['name', 'business_section_name', 'description']