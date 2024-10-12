from rest_framework import viewsets, permissions

from . import serializers
from . import models


from core.__permissions import IsUserOrReadOnly, IsOwnerOrReadOnly

class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet for the Ingredient class"""

    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]


class MenuViewSet(viewsets.ModelViewSet):
    """ViewSet for the Menu class"""

    queryset = models.Menu.objects.all()
    serializer_class = serializers.MenuSerializer
    permission_classes = [permissions.IsAuthenticated]


class MenuItemViewSet(viewsets.ModelViewSet):
    """ViewSet for the MenuItem class"""

    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class RestaurantViewSet(viewsets.ModelViewSet):
    """ViewSet for the Restaurant class"""

    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
class RestaurantStoreViewSet(viewsets.ModelViewSet):
    """ViewSet for the Restaurant's Store class"""

    queryset = models.RestaurantStore.objects.all()
    serializer_class = serializers.RestaurantStoreSerializer
    permission_classes = [IsOwnerOrReadOnly]


class RestaurantStockViewSet(viewsets.ModelViewSet):
    """ViewSet for the Restaurant's Store class"""

    queryset = models.RestaurantStock.objects.all()
    serializer_class = serializers.RestaurantStockSerializer
    permission_classes = [IsOwnerOrReadOnly]


''' 
class ChefViewSet(viewsets.ModelViewSet):
    """ViewSet for the Chef class"""

    queryset = models.Chef.objects.all()
    serializer_class = serializers.ChefSerializer
    permission_classes = [permissions.IsAuthenticated]

 '''
class StaffViewSet(viewsets.ModelViewSet):
    """ViewSet for the Staff class"""

    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOrReadOnly]
