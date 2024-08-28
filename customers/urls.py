from django.urls import path, include
from rest_framework import routers

from . import api
from . import views
from . import htmx


router = routers.DefaultRouter()
router.register("Order", api.OrderViewSet)
router.register("Customer", api.CustomerViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path(
        "customers/Order/",
        views.OrderListView.as_view(),
        name="customers_Order_list",
    ),
    path(
        "customers/Order/create/",
        views.OrderCreateView.as_view(),
        name="customers_Order_create",
    ),
    path(
        "customers/Order/detail/<int:pk>/",
        views.OrderDetailView.as_view(),
        name="customers_Order_detail",
    ),
    path(
        "customers/Order/update/<int:pk>/",
        views.OrderUpdateView.as_view(),
        name="customers_Order_update",
    ),
    path(
        "customers/Order/delete/<int:pk>/",
        views.OrderDeleteView.as_view(),
        name="customers_Order_delete",
    ),
    path(
        "customers/Customer/",
        views.CustomerListView.as_view(),
        name="customers_Customer_list",
    ),
    path(
        "customers/Customer/create/",
        views.CustomerCreateView.as_view(),
        name="customers_Customer_create",
    ),
    path(
        "customers/Customer/detail/<int:pk>/",
        views.CustomerDetailView.as_view(),
        name="customers_Customer_detail",
    ),
    path(
        "customers/Customer/update/<int:pk>/",
        views.CustomerUpdateView.as_view(),
        name="customers_Customer_update",
    ),
    path(
        "customers/Customer/delete/<int:pk>/",
        views.CustomerDeleteView.as_view(),
        name="customers_Customer_delete",
    ),
    path(
        "customers/htmx/Order/",
        htmx.HTMXOrderListView.as_view(),
        name="customers_Order_htmx_list",
    ),
    path(
        "customers/htmx/Order/create/",
        htmx.HTMXOrderCreateView.as_view(),
        name="customers_Order_htmx_create",
    ),
    path(
        "customers/htmx/Order/delete/<int:pk>/",
        htmx.HTMXOrderDeleteView.as_view(),
        name="customers_Order_htmx_delete",
    ),
    path(
        "customers/htmx/Customer/",
        htmx.HTMXCustomerListView.as_view(),
        name="customers_Customer_htmx_list",
    ),
    path(
        "customers/htmx/Customer/create/",
        htmx.HTMXCustomerCreateView.as_view(),
        name="customers_Customer_htmx_create",
    ),
    path(
        "customers/htmx/Customer/delete/<int:pk>/",
        htmx.HTMXCustomerDeleteView.as_view(),
        name="customers_Customer_htmx_delete",
    ),
)
