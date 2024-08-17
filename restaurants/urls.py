from django.urls import path, include
from rest_framework import routers

from . import api
from . import views
from . import htmx


router = routers.DefaultRouter()
router.register("Ingredient", api.IngredientViewSet)
router.register("Menu", api.MenuViewSet)
router.register("MenuItem", api.MenuItemViewSet)
router.register("Restaurant", api.RestaurantViewSet)
#router.register("Chef", api.ChefViewSet)
router.register("Staff", api.StaffViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("restaurants/Ingredient/", views.IngredientListView.as_view(), name="restaurant_Ingredient_list"),
    path("restaurants/Ingredient/create/", views.IngredientCreateView.as_view(), name="restaurant_Ingredient_create"),
    path("restaurants/Ingredient/detail/<int:pk>/", views.IngredientDetailView.as_view(), name="restaurant_Ingredient_detail"),
    path("restaurants/Ingredient/update/<int:pk>/", views.IngredientUpdateView.as_view(), name="restaurant_Ingredient_update"),
    path("restaurants/Ingredient/delete/<int:pk>/", views.IngredientDeleteView.as_view(), name="restaurant_Ingredient_delete"),
    path("restaurants/Menu/", views.MenuListView.as_view(), name="restaurant_Menu_list"),
    path("restaurants/Menu/create/", views.MenuCreateView.as_view(), name="restaurant_Menu_create"),
    path("restaurants/Menu/detail/<int:pk>/", views.MenuDetailView.as_view(), name="restaurant_Menu_detail"),
    path("restaurants/Menu/update/<int:pk>/", views.MenuUpdateView.as_view(), name="restaurant_Menu_update"),
    path("restaurants/Menu/delete/<int:pk>/", views.MenuDeleteView.as_view(), name="restaurant_Menu_delete"),
    path("restaurants/MenuItem/", views.MenuItemListView.as_view(), name="restaurant_MenuItem_list"),
    path("restaurants/MenuItem/create/", views.MenuItemCreateView.as_view(), name="restaurant_MenuItem_create"),
    path("restaurants/MenuItem/detail/<int:pk>/", views.MenuItemDetailView.as_view(), name="restaurant_MenuItem_detail"),
    path("restaurants/MenuItem/update/<int:pk>/", views.MenuItemUpdateView.as_view(), name="restaurant_MenuItem_update"),
    path("restaurants/MenuItem/delete/<int:pk>/", views.MenuItemDeleteView.as_view(), name="restaurant_MenuItem_delete"),
    path("restaurants/Restaurant/", views.RestaurantListView.as_view(), name="restaurant_Restaurant_list"),
    path("restaurants/Restaurant/create/", views.RestaurantCreateView.as_view(), name="restaurant_Restaurant_create"),
    path("restaurants/Restaurant/detail/<int:pk>/", views.RestaurantDetailView.as_view(), name="restaurant_Restaurant_detail"),
    path("restaurants/Restaurant/update/<int:pk>/", views.RestaurantUpdateView.as_view(), name="restaurant_Restaurant_update"),
    path("restaurants/Restaurant/delete/<int:pk>/", views.RestaurantDeleteView.as_view(), name="restaurant_Restaurant_delete"),
    #path("restaurants/Chef/", views.ChefListView.as_view(), name="restaurant_Chef_list"),
    #path("restaurants/Chef/create/", views.ChefCreateView.as_view(), name="restaurant_Chef_create"),
    #path("restaurants/Chef/detail/<int:pk>/", views.ChefDetailView.as_view(), name="restaurant_Chef_detail"),
    #path("restaurants/Chef/update/<int:pk>/", views.ChefUpdateView.as_view(), name="restaurant_Chef_update"),
    #path("restaurants/Chef/delete/<int:pk>/", views.ChefDeleteView.as_view(), name="restaurant_Chef_delete"),
    path("restaurants/Staff/", views.StaffListView.as_view(), name="restaurant_Staff_list"),
    path("restaurants/Staff/create/", views.StaffCreateView.as_view(), name="restaurant_Staff_create"),
    path("restaurants/Staff/detail/<int:pk>/", views.StaffDetailView.as_view(), name="restaurant_Staff_detail"),
    path("restaurants/Staff/update/<int:pk>/", views.StaffUpdateView.as_view(), name="restaurant_Staff_update"),
    path("restaurants/Staff/delete/<int:pk>/", views.StaffDeleteView.as_view(), name="restaurant_Staff_delete"),

    path("restaurants/htmx/Ingredient/", htmx.HTMXIngredientListView.as_view(), name="restaurant_Ingredient_htmx_list"),
    path("restaurants/htmx/Ingredient/create/", htmx.HTMXIngredientCreateView.as_view(), name="restaurant_Ingredient_htmx_create"),
    path("restaurants/htmx/Ingredient/delete/<int:pk>/", htmx.HTMXIngredientDeleteView.as_view(), name="restaurant_Ingredient_htmx_delete"),
    path("restaurants/htmx/Menu/", htmx.HTMXMenuListView.as_view(), name="restaurant_Menu_htmx_list"),
    path("restaurants/htmx/Menu/create/", htmx.HTMXMenuCreateView.as_view(), name="restaurant_Menu_htmx_create"),
    path("restaurants/htmx/Menu/delete/<int:pk>/", htmx.HTMXMenuDeleteView.as_view(), name="restaurant_Menu_htmx_delete"),
    path("restaurants/htmx/MenuItem/", htmx.HTMXMenuItemListView.as_view(), name="restaurant_MenuItem_htmx_list"),
    path("restaurants/htmx/MenuItem/create/", htmx.HTMXMenuItemCreateView.as_view(), name="restaurant_MenuItem_htmx_create"),
    path("restaurants/htmx/MenuItem/delete/<int:pk>/", htmx.HTMXMenuItemDeleteView.as_view(), name="restaurant_MenuItem_htmx_delete"),
    path("restaurants/htmx/Restaurant/", htmx.HTMXRestaurantListView.as_view(), name="restaurant_Restaurant_htmx_list"),
    path("restaurants/htmx/Restaurant/create/", htmx.HTMXRestaurantCreateView.as_view(), name="restaurant_Restaurant_htmx_create"),
    path("restaurants/htmx/Restaurant/delete/<int:pk>/", htmx.HTMXRestaurantDeleteView.as_view(), name="restaurant_Restaurant_htmx_delete"),
    #path("restaurants/htmx/Chef/", htmx.HTMXChefListView.as_view(), name="restaurant_Chef_htmx_list"),
    #path("restaurants/htmx/Chef/create/", htmx.HTMXChefCreateView.as_view(), name="restaurant_Chef_htmx_create"),
    #path("restaurants/htmx/Chef/delete/<int:pk>/", htmx.HTMXChefDeleteView.as_view(), name="restaurant_Chef_htmx_delete"),
    path("restaurants/htmx/Staff/", htmx.HTMXStaffListView.as_view(), name="restaurant_Staff_htmx_list"),
    path("restaurants/htmx/Staff/create/", htmx.HTMXStaffCreateView.as_view(), name="restaurant_Staff_htmx_create"),
    path("restaurants/htmx/Staff/delete/<int:pk>/", htmx.HTMXStaffDeleteView.as_view(), name="restaurant_Staff_htmx_delete"),
)
