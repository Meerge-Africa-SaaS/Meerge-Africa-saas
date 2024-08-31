from rest_framework import viewsets, permissions

from . import serializers
from . import models


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Category class"""

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ItemViewSet(viewsets.ModelViewSet):
    """ViewSet for the Item class"""

    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class StockViewSet(viewsets.ModelViewSet):
    """ViewSet for the Stock class"""

    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer
    permission_classes = [permissions.IsAuthenticated]


class SupplierViewSet(viewsets.ModelViewSet):
    """ViewSet for the Supplier class"""

    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]


class SupplyManagerViewSet(viewsets.ModelViewSet):
    """ViewSet for the SupplyManager class"""

    queryset = models.SupplyManager.objects.all()
    serializer_class = serializers.SupplyManagerSerializer
    permission_classes = [permissions.IsAuthenticated]
