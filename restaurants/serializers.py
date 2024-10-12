from rest_framework import serializers

from . import models


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = [
            "last_updated",
            "name",
            "created",
            "menu_item",
        ]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = [
            "date_from",
            "created",
            "name",
            "date_to",
            "last_updated",
        ]


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = [
            "name",
            "price",
            "created",
            "last_updated",
            "menu",
        ]


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = [
            "address",
            "created",
            "name",
            "last_updated",
            "city",
            "owner",
            "custom_link"
        ]


class RestaurantStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantStore
        fields = [
            "restaurant",
            "name",
            "description",
            "image",
            "section_name"
        ]

""" 
class ChefSerializer(serializers.ModelSerializer):

class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chef
        fields = [
            "created",
            "last_updated",
            "restaurants",
        ]
 """


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Staff
        fields = [
            "created",
            "last_updated",
            "restaurants",
        ]
