from django.urls import include, path
from rest_framework import routers

from restaurants import onboarding, pages, registration

from . import api, htmx, views

router = routers.DefaultRouter()
router.register("Ingredient", api.IngredientViewSet)
router.register("Menu", api.MenuViewSet)
router.register("MenuItem", api.MenuItemViewSet)
router.register("Restaurant", api.RestaurantViewSet)
router.register("RestaurantStore", api.RestaurantStoreViewSet)
router.register("RestaurantStock", api.RestaurantStockViewSet)

# router.register("Chef", api.ChefViewSet)
router.register("Staff", api.StaffViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path(
        "signup/",
        registration.RegistrationView.as_view(),
        name="restaurant_signup",
    ),
    path(
        "email_verification/done/",
        registration.EmailVerificationDoneView.as_view(),
        name="restaurant_email_verification_done",
    ),
    path(
        "onboarding/",
        onboarding.OnboardingView.as_view(),
        name="restaurant_onboarding",
    ),
    path(
        "onboarding/wizard",
        onboarding.OnboardingWizardView.as_view(),
        name="restaurant_onboarding_wizard",
    ),
    path(
        "Ingredient/",
        views.IngredientListView.as_view(),
        name="restaurant_Ingredient_list",
    ),
    path(
        "Ingredient/create/",
        views.IngredientCreateView.as_view(),
        name="restaurant_Ingredient_create",
    ),
    path(
        "Ingredient/detail/<int:pk>/",
        views.IngredientDetailView.as_view(),
        name="restaurant_Ingredient_detail",
    ),
    path(
        "Ingredient/update/<int:pk>/",
        views.IngredientUpdateView.as_view(),
        name="restaurant_Ingredient_update",
    ),
    path(
        "Ingredient/delete/<int:pk>/",
        views.IngredientDeleteView.as_view(),
        name="restaurant_Ingredient_delete",
    ),
    path(
        "MenuCategory/",
        views.MenuCategoryListView.as_view(),
        name="restaurant_MenuCategory_list",
    ),
    path(
        "MenuCategory/create/",
        views.MenuCategoryCreateView.as_view(),
        name="restaurant_MenuCategory_create",
    ),
    path(
        "MenuCategory/detail/<int:pk>/",
        views.MenuCategoryDetailView.as_view(),
        name="restaurant_MenuCategory_detail",
    ),
    path(
        "MenuCategory/update/<int:pk>/",
        views.MenuCategoryUpdateView.as_view(),
        name="restaurant_MenuCategory_update",
    ),
    path(
        "MenuCategory/delete/<int:pk>/",
        views.MenuCategoryDeleteView.as_view(),
        name="restaurant_MenuCategory_delete",
    ),
    path(
        "Menu/",
        views.MenuListView.as_view(),
        name="restaurant_Menu_list",
    ),
    path(
        "Menu/create/",
        views.MenuCreateView.as_view(),
        name="restaurant_Menu_create",
    ),
    path(
        "Menu/detail/<int:pk>/",
        views.MenuDetailView.as_view(),
        name="restaurant_Menu_detail",
    ),
    path(
        "Menu/update/<int:pk>/",
        views.MenuUpdateView.as_view(),
        name="restaurant_Menu_update",
    ),
    path(
        "Menu/delete/<int:pk>/",
        views.MenuDeleteView.as_view(),
        name="restaurant_Menu_delete",
    ),
    path(
        "AddOn/",
        views.AddOnListView.as_view(),
        name="restaurant_AddOn_list",
    ),
    path(
        "AddOn/create/",
        views.AddOnCreateView.as_view(),
        name="restaurant_AddOn_create",
    ),
    path(
        "AddOn/detail/<int:pk>/",
        views.AddOnDetailView.as_view(),
        name="restaurant_AddOn_detail",
    ),
    path(
        "AddOn/update/<int:pk>/",
        views.AddOnUpdateView.as_view(),
        name="restaurant_AddOn_update",
    ),
    path(
        "AddOn/delete/<int:pk>/",
        views.AddOnDeleteView.as_view(),
        name="restaurant_AddOn_delete",
    ),
    path(
        "MenuItem/",
        views.MenuItemListView.as_view(),
        name="restaurant_MenuItem_list",
    ),
    path(
        "MenuItem/create/",
        views.MenuItemCreateView.as_view(),
        name="restaurant_MenuItem_create",
    ),
    path(
        "MenuItem/detail/<int:pk>/",
        views.MenuItemDetailView.as_view(),
        name="restaurant_MenuItem_detail",
    ),
    path(
        "MenuItem/update/<int:pk>/",
        views.MenuItemUpdateView.as_view(),
        name="restaurant_MenuItem_update",
    ),
    path(
        "MenuItem/delete/<int:pk>/",
        views.MenuItemDeleteView.as_view(),
        name="restaurant_MenuItem_delete",
    ),
    path(
        "Restaurant/",
        views.RestaurantListView.as_view(),
        name="restaurant_Restaurant_list",
    ),
    path(
        "Restaurant/create/",
        views.RestaurantCreateView.as_view(),
        name="restaurant_Restaurant_create",
    ),
    path(
        "Restaurant/detail/<int:pk>/",
        views.RestaurantDetailView.as_view(),
        name="restaurant_Restaurant_detail",
    ),
    path(
        "Restaurant/update/<int:pk>/",
        views.RestaurantUpdateView.as_view(),
        name="restaurant_Restaurant_update",
    ),
    path(
        "Restaurant/delete/<int:pk>/",
        views.RestaurantDeleteView.as_view(),
        name="restaurant_Restaurant_delete",
    ),
    # TODO: Add Chef views
    # path(
    #     "Chef/",
    #     views.ChefListView.as_view(),
    #     name="restaurant_Chef_list",
    # ),
    # path(
    #     "Chef/create/",
    #     views.ChefCreateView.as_view(),
    #     name="restaurant_Chef_create",
    # ),
    # path(
    #     "Chef/detail/<int:pk>/",
    #     views.ChefDetailView.as_view(),
    #     name="restaurant_Chef_detail",
    # ),
    # path(
    #     "Chef/update/<int:pk>/",
    #     views.ChefUpdateView.as_view(),
    #     name="restaurant_Chef_update",
    # ),
    # path(
    #     "Chef/delete/<int:pk>/",
    #     views.ChefDeleteView.as_view(),
    #     name="restaurant_Chef_delete",
    # ),
    path(
        "Staff/",
        views.StaffListView.as_view(),
        name="restaurant_Staff_list",
    ),
    path(
        "Staff/create/",
        views.StaffCreateView.as_view(),
        name="restaurant_Staff_create",
    ),
    path(
        "Staff/detail/<int:pk>/",
        views.StaffDetailView.as_view(),
        name="restaurant_Staff_detail",
    ),
    path(
        "Staff/update/<int:pk>/",
        views.StaffUpdateView.as_view(),
        name="restaurant_Staff_update",
    ),
    path(
        "Staff/delete/<int:pk>/",
        views.StaffDeleteView.as_view(),
        name="restaurant_Staff_delete",
    ),
    path(
        "htmx/Ingredient/",
        htmx.HTMXIngredientListView.as_view(),
        name="restaurant_Ingredient_htmx_list",
    ),
    path(
        "htmx/Ingredient/create/",
        htmx.HTMXIngredientCreateView.as_view(),
        name="restaurant_Ingredient_htmx_create",
    ),
    path(
        "htmx/Ingredient/delete/<int:pk>/",
        htmx.HTMXIngredientDeleteView.as_view(),
        name="restaurant_Ingredient_htmx_delete",
    ),
    path(
        "htmx/Menu/",
        htmx.HTMXMenuListView.as_view(),
        name="restaurant_Menu_htmx_list",
    ),
    path(
        "htmx/Menu/create/",
        htmx.HTMXMenuCreateView.as_view(),
        name="restaurant_Menu_htmx_create",
    ),
    path(
        "htmx/Menu/delete/<int:pk>/",
        htmx.HTMXMenuDeleteView.as_view(),
        name="restaurant_Menu_htmx_delete",
    ),
    path(
        "htmx/MenuItem/",
        htmx.HTMXMenuItemListView.as_view(),
        name="restaurant_MenuItem_htmx_list",
    ),
    path(
        "htmx/MenuItem/create/",
        htmx.HTMXMenuItemCreateView.as_view(),
        name="restaurant_MenuItem_htmx_create",
    ),
    path(
        "htmx/MenuItem/delete/<int:pk>/",
        htmx.HTMXMenuItemDeleteView.as_view(),
        name="restaurant_MenuItem_htmx_delete",
    ),
    path(
        "htmx/Restaurant/",
        htmx.HTMXRestaurantListView.as_view(),
        name="restaurant_Restaurant_htmx_list",
    ),
    path(
        "htmx/Restaurant/create/",
        htmx.HTMXRestaurantCreateView.as_view(),
        name="restaurant_Restaurant_htmx_create",
    ),
    path(
        "htmx/Restaurant/delete/<int:pk>/",
        htmx.HTMXRestaurantDeleteView.as_view(),
        name="restaurant_Restaurant_htmx_delete",
    ),
    path(
        "htmx/Restaurant/logo/<int:pk>/",
        htmx.HTMXRestaurantLogoView.as_view(),
        name="restaurant_Restaurant_htmx_logo",
    ),
    path(
        "htmx/Restaurant/cover/<int:pk>/",
        htmx.HTMXRestaurantCoverView.as_view(),
        name="restaurant_Restaurant_htmx_cover",
    ),
    # TODO: Add Chef views
    # path(
    #     "htmx/Chef/",
    #     htmx.HTMXChefListView.as_view(),
    #     name="restaurant_Chef_htmx_list",
    # ),
    # path(
    #     "htmx/Chef/create/",
    #     htmx.HTMXChefCreateView.as_view(),
    #     name="restaurant_Chef_htmx_create",
    # ),
    # path(
    #     "htmx/Chef/delete/<int:pk>/",
    #     htmx.HTMXChefDeleteView.as_view(),
    #     name="restaurant_Chef_htmx_delete",
    # ),
    # path(
    #     "htmx/Staff/",
    #     htmx.HTMXStaffListView.as_view(),
    #     name="restaurant_Staff_htmx_list",
    # ),
    # path(
    #     "htmx/Staff/create/",
    #     htmx.HTMXStaffCreateView.as_view(),
    #     name="restaurant_Staff_htmx_create",
    # ),
    # path(
    #     "htmx/Staff/delete/<int:pk>/",
    #     htmx.HTMXStaffDeleteView.as_view(),
    #     name="restaurant_Staff_htmx_delete",
    # ),
    path("", pages.RestaurantRedirectView.as_view(), name="restaurant_redirect"),
    path("<slug:restaurant>/", include("restaurants.pages", namespace="pages")),
)
