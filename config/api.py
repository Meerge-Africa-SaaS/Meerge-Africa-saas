from django.urls import include, path
from rest_framework import routers


from customers.api import OrderViewSet, CustomerViewSet
from restaurants.api import (
    IngredientViewSet,
    MenuViewSet,
    MenuItemViewSet,
    RestaurantViewSet,
    ChefViewSet,
    StaffViewSet,
)

router = routers.DefaultRouter()

router.register("Ingredient", IngredientViewSet)
router.register("Menu", MenuViewSet)
router.register("MenuItem", MenuItemViewSet)
router.register("Restaurant", RestaurantViewSet)
router.register("Chef", ChefViewSet)
router.register("Staff", StaffViewSet)

router.register("Order", OrderViewSet)
router.register("Customer", CustomerViewSet)

urlpatterns = (path("api/v1/", include(router.urls)),)
