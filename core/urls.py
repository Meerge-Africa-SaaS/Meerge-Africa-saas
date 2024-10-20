from django.urls import include, path
from ninja import NinjaAPI
from rest_framework import routers

from core.auth_api.api import router as auth_router
from core.auth_api.password_management import p_router
from core.auth_api.onboarding import router as onboarding_router
from banking.ninja_api import router as banking_router
from core.auth_api.token_management import AuthBearer

from . import api, htmx, views

router = routers.DefaultRouter()
router.register("User", api.UserViewSet)

### NINJA API ROUTES
ninjaapi = NinjaAPI()  # auth=AuthBearer())
ninjaapi.add_router("auth-api", auth_router)
ninjaapi.add_router("password", p_router)
ninjaapi.add_router("onboarding", onboarding_router)
ninjaapi.add_router("banking", banking_router)


urlpatterns = (
    path("authenticate/", ninjaapi.urls, name="n-api"),
    path("api/v1/", include(router.urls)),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path("User/", views.UserListView.as_view(), name="core_User_list"),
    path("User/create/", views.UserCreateView.as_view(), name="core_User_create"),
    path(
        "User/detail/<int:pk>/", views.UserDetailView.as_view(), name="core_User_detail"
    ),
    path(
        "User/update/<int:pk>/", views.UserUpdateView.as_view(), name="core_User_update"
    ),
    path(
        "User/delete/<int:pk>/", views.UserDeleteView.as_view(), name="core_User_delete"
    ),
    path(
        "User/forgot-password/",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "User/forgot-password/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "User/forgot-password/confirm/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "User/forgot-password/complete/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("htmx/User/", htmx.HTMXUserListView.as_view(), name="core_User_htmx_list"),
    path(
        "htmx/User/create/",
        htmx.HTMXUserCreateView.as_view(),
        name="core_User_htmx_create",
    ),
    path(
        "htmx/User/delete/<int:pk>/",
        htmx.HTMXUserDeleteView.as_view(),
        name="core_User_htmx_delete",
    ),
)
