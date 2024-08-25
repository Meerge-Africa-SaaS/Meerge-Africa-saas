from django.urls import path, include
from rest_framework import routers

from . import api
from . import views
from . import htmx


router = routers.DefaultRouter()
router.register("DeliveryAgent", api.DeliveryAgentViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path(
        "orders/DeliveryAgent/",
        views.DeliveryAgentListView.as_view(),
        name="orders_DeliveryAgent_list",
    ),
    path(
        "orders/DeliveryAgent/create/",
        views.DeliveryAgentCreateView.as_view(),
        name="orders_DeliveryAgent_create",
    ),
    path(
        "orders/DeliveryAgent/detail/<int:pk>/",
        views.DeliveryAgentDetailView.as_view(),
        name="orders_DeliveryAgent_detail",
    ),
    path(
        "orders/DeliveryAgent/update/<int:pk>/",
        views.DeliveryAgentUpdateView.as_view(),
        name="orders_DeliveryAgent_update",
    ),
    path(
        "orders/DeliveryAgent/delete/<int:pk>/",
        views.DeliveryAgentDeleteView.as_view(),
        name="orders_DeliveryAgent_delete",
    ),
    path(
        "orders/htmx/DeliveryAgent/",
        htmx.HTMXDeliveryAgentListView.as_view(),
        name="orders_DeliveryAgent_htmx_list",
    ),
    path(
        "orders/htmx/DeliveryAgent/create/",
        htmx.HTMXDeliveryAgentCreateView.as_view(),
        name="orders_DeliveryAgent_htmx_create",
    ),
    path(
        "orders/htmx/DeliveryAgent/delete/<int:pk>/",
        htmx.HTMXDeliveryAgentDeleteView.as_view(),
        name="orders_DeliveryAgent_htmx_delete",
    ),
)
