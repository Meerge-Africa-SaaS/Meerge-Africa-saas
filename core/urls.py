from django.urls import include, path
from rest_framework import routers

from . import api, htmx, views

router = routers.DefaultRouter()
router.register("User", api.UserViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("User/", views.UserListView.as_view(), name="core_User_list"),
    path("User/create/", views.UserCreateView.as_view(), name="core_User_create"),
    path("User/detail/<str:pk>/", views.UserDetailView.as_view(), name="core_User_detail"),
    path("User/update/<str:pk>/", views.UserUpdateView.as_view(), name="core_User_update"),
    path("User/delete/<str:pk>/", views.UserDeleteView.as_view(), name="core_User_delete"),

    path("core_User_signin"),

    path("htmx/User/", htmx.HTMXUserListView.as_view(), name="core_User_htmx_list"),
    path("htmx/User/create/", htmx.HTMXUserCreateView.as_view(), name="core_User_htmx_create"),
    path("htmx/User/delete/<str:pk>/", htmx.HTMXUserDeleteView.as_view(), name="core_User_htmx_delete"),
)
