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
        registration.signup,
        name="restaurant_signup",
    ),
    path(
        "signup/<str:invite_key>/",
        registration.InvitationRegistrationView.as_view(),
        name="restaurant_staff_registration",
    ),
    path(
        "invitation/accept/<str:key>/",
        onboarding.AcceptInviteView.as_view(),
        name="restaurant_accept_invite",
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
        "<int:restaurant>/addons/",
        views.existing_addons,
        name="restaurant_existing_addons",
    ),
    path(
        "<int:restaurant>/addons/search/",
        views.search_addons,
        name="restaurant_search_addons",
    ),
    path(
        "addon/<int:addon_id>/select/",
        views.select_addon,
        name="restaurant_select_addon",
    ),
    path(
        "addon/<int:addon_id>/remove/",
        views.remove_addon,
        name="restaurant_remove_addon",
    ),
    path(
        "<int:restaurant>/addon/create/",
        views.create_addon,
        name="restaurant_create_addon",
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
    path("<slug:restaurant>/invite", onboarding.SendInviteView.as_view(), name="restaurant-invite-employee"),
    path("<slug:restaurant>/", include("restaurants.pages", namespace="pages")),
)
