from django.urls import include, path
from rest_framework import routers

from core.api import UserViewSet
from customers.api import CustomerViewSet, OrderViewSet
from inventory.api import (
    CategoryViewSet,
    ItemViewSet,
    StockViewSet,
    SupplierViewSet,
    SupplyManagerViewSet,
)
from orders.api import DeliveryAgentViewSet
from restaurants.api import (
    # ChefViewSet,
    IngredientViewSet,
    MenuItemViewSet,
    MenuViewSet,
    RestaurantViewSet,
    StaffViewSet,
)

router = routers.DefaultRouter()

router.register("Ingredient", IngredientViewSet)
router.register("Menu", MenuViewSet)
router.register("MenuItem", MenuItemViewSet)
router.register("Restaurant", RestaurantViewSet)
# router.register("Chef", ChefViewSet)
router.register("Staff", StaffViewSet)

router.register("Order", OrderViewSet)
router.register("Customer", CustomerViewSet)

router.register("User", UserViewSet)
router.register("Order", OrderViewSet)
router.register("Customer", CustomerViewSet)

router.register("DeliveryAgent", DeliveryAgentViewSet)

router.register("Category", CategoryViewSet)
router.register("Item", ItemViewSet)
router.register("Stock", StockViewSet)
router.register("Supplier", SupplierViewSet)
router.register("SupplyManager", SupplyManagerViewSet)

urlpatterns = (path("api/v1/", include(router.urls)),)
