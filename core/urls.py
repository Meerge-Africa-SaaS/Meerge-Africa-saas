from django.urls import include, path
from ninja import NinjaAPI
from rest_framework import routers

from core.auth_api.api import router as auth_router
from core.auth_api.token_management import AuthBearer

from . import api, htmx, views

router = routers.DefaultRouter()
router.register("User", api.UserViewSet)


### NINJA API ROUTES
api = NinjaAPI(auth=AuthBearer())
api.add_router("auth-api", auth_router)

urlpatterns = (
    path("authenticate/", api.urls, name="n-api"),
    path("api/v1/", include(router.urls)),
    path("core/User/signin/", views.UserSigninView.as_view(), name="core_User_signin"),
    path("core/User/", views.UserListView.as_view(), name="core_User_list"),
    path("core/User/create/", views.UserCreateView.as_view(), name="core_User_create"),
    path(
        "core/User/detail/<int:pk>/",
        views.UserDetailView.as_view(),
        name="core_User_detail",
    ),
    path(
        "core/User/update/<int:pk>/",
        views.UserUpdateView.as_view(),
        name="core_User_update",
    ),
    path(
        "core/User/delete/<int:pk>/",
        views.UserDeleteView.as_view(),
        name="core_User_delete",
    ),
    path(
        "core/htmx/User/", htmx.HTMXUserListView.as_view(), name="core_User_htmx_list"
    ),
    path(
        "core/htmx/User/create/",
        htmx.HTMXUserCreateView.as_view(),
        name="core_User_htmx_create",
    ),
    path(
        "core/htmx/User/delete/<int:pk>/",
        htmx.HTMXUserDeleteView.as_view(),
        name="core_User_htmx_delete",
    ),
)
