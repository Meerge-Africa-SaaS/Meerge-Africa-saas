from django.urls import path, include
from rest_framework import routers

from . import api
from . import views
from . import htmx


router = routers.DefaultRouter()
router.register("Category", api.CategoryViewSet)
router.register("Item", api.ItemViewSet)
router.register("Stock", api.StockViewSet)
router.register("Supplier", api.SupplierViewSet)
router.register("SupplyManager", api.SupplyManagerViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("inventory/Category/", views.CategoryListView.as_view(), name="inventory_Category_list"),
    path("inventory/Category/create/", views.CategoryCreateView.as_view(), name="inventory_Category_create"),
    path("inventory/Category/detail/<int:pk>/", views.CategoryDetailView.as_view(), name="inventory_Category_detail"),
    path("inventory/Category/update/<int:pk>/", views.CategoryUpdateView.as_view(), name="inventory_Category_update"),
    path("inventory/Category/delete/<int:pk>/", views.CategoryDeleteView.as_view(), name="inventory_Category_delete"),
    path("inventory/Item/", views.ItemListView.as_view(), name="inventory_Item_list"),
    path("inventory/Item/create/", views.ItemCreateView.as_view(), name="inventory_Item_create"),
    path("inventory/Item/detail/<int:pk>/", views.ItemDetailView.as_view(), name="inventory_Item_detail"),
    path("inventory/Item/update/<int:pk>/", views.ItemUpdateView.as_view(), name="inventory_Item_update"),
    path("inventory/Item/delete/<int:pk>/", views.ItemDeleteView.as_view(), name="inventory_Item_delete"),
    path("inventory/Stock/", views.StockListView.as_view(), name="inventory_Stock_list"),
    path("inventory/Stock/create/", views.StockCreateView.as_view(), name="inventory_Stock_create"),
    path("inventory/Stock/detail/<int:pk>/", views.StockDetailView.as_view(), name="inventory_Stock_detail"),
    path("inventory/Stock/update/<int:pk>/", views.StockUpdateView.as_view(), name="inventory_Stock_update"),
    path("inventory/Stock/delete/<int:pk>/", views.StockDeleteView.as_view(), name="inventory_Stock_delete"),
    path("inventory/Supplier/", views.SupplierListView.as_view(), name="inventory_Supplier_list"),
    path("inventory/Supplier/create/", views.SupplierCreateView.as_view(), name="inventory_Supplier_create"),
    path("inventory/Supplier/detail/<int:pk>/", views.SupplierDetailView.as_view(), name="inventory_Supplier_detail"),
    path("inventory/Supplier/update/<int:pk>/", views.SupplierUpdateView.as_view(), name="inventory_Supplier_update"),
    path("inventory/Supplier/delete/<int:pk>/", views.SupplierDeleteView.as_view(), name="inventory_Supplier_delete"),
    path("inventory/SupplyManager/", views.SupplyManagerListView.as_view(), name="inventory_SupplyManager_list"),
    path("inventory/SupplyManager/create/", views.SupplyManagerCreateView.as_view(), name="inventory_SupplyManager_create"),
    path("inventory/SupplyManager/detail/<int:pk>/", views.SupplyManagerDetailView.as_view(), name="inventory_SupplyManager_detail"),
    path("inventory/SupplyManager/update/<int:pk>/", views.SupplyManagerUpdateView.as_view(), name="inventory_SupplyManager_update"),
    path("inventory/SupplyManager/delete/<int:pk>/", views.SupplyManagerDeleteView.as_view(), name="inventory_SupplyManager_delete"),

    path("inventory/htmx/Category/", htmx.HTMXCategoryListView.as_view(), name="inventory_Category_htmx_list"),
    path("inventory/htmx/Category/create/", htmx.HTMXCategoryCreateView.as_view(), name="inventory_Category_htmx_create"),
    path("inventory/htmx/Category/delete/<int:pk>/", htmx.HTMXCategoryDeleteView.as_view(), name="inventory_Category_htmx_delete"),
    path("inventory/htmx/Item/", htmx.HTMXItemListView.as_view(), name="inventory_Item_htmx_list"),
    path("inventory/htmx/Item/create/", htmx.HTMXItemCreateView.as_view(), name="inventory_Item_htmx_create"),
    path("inventory/htmx/Item/delete/<int:pk>/", htmx.HTMXItemDeleteView.as_view(), name="inventory_Item_htmx_delete"),
    path("inventory/htmx/Stock/", htmx.HTMXStockListView.as_view(), name="inventory_Stock_htmx_list"),
    path("inventory/htmx/Stock/create/", htmx.HTMXStockCreateView.as_view(), name="inventory_Stock_htmx_create"),
    path("inventory/htmx/Stock/delete/<int:pk>/", htmx.HTMXStockDeleteView.as_view(), name="inventory_Stock_htmx_delete"),
    path("inventory/htmx/Supplier/", htmx.HTMXSupplierListView.as_view(), name="inventory_Supplier_htmx_list"),
    path("inventory/htmx/Supplier/create/", htmx.HTMXSupplierCreateView.as_view(), name="inventory_Supplier_htmx_create"),
    path("inventory/htmx/Supplier/delete/<int:pk>/", htmx.HTMXSupplierDeleteView.as_view(), name="inventory_Supplier_htmx_delete"),
    path("inventory/htmx/SupplyManager/", htmx.HTMXSupplyManagerListView.as_view(), name="inventory_SupplyManager_htmx_list"),
    path("inventory/htmx/SupplyManager/create/", htmx.HTMXSupplyManagerCreateView.as_view(), name="inventory_SupplyManager_htmx_create"),
    path("inventory/htmx/SupplyManager/delete/<int:pk>/", htmx.HTMXSupplyManagerDeleteView.as_view(), name="inventory_SupplyManager_htmx_delete"),

)
