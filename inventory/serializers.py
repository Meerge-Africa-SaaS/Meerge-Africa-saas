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
        
    
class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemCategory
        fields = [
            "created",
            "name",
            "last_updated",
        ]


class ItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name')
    category = serializers.CharField(source='item.category.name')
    unit_of_measure = serializers.CharField(source='item.unit_of_measure')

    class Meta:
        model = models.Item
        fields = [
            'item_name',          
            #'product_image',      
            'category',           
            #'availability_status',
            'price',            
            #'quantity',          
            'unit_of_measure',   
        ]
class ViewStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = [
            'product_name',
            'product_image',
            'product_category',
            'price',
            'unit_available',
            'unit_of_measure',
            'low_stock_alert_unit',
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
            "SKU_number",
            "product_name",
            "product_image",
            "product_category",
            "manufacture_name",
            "price",
            "unit_available",
            "size",
            "weight",
            #"availability_status",
            "discount_percentage",
            #"delivery_time_estimate",
            #"pickup_option",
            #"password",
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
            "owner",
            "last_updated",
            "city",
            "email",
            "phone_number",
            "cac_reg_number",
            "cac_certificate",
            "business_license",
            #"category",
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
            #"supplier",
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "supply_business",
        ]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = ['name', 'business_section_name', 'description']