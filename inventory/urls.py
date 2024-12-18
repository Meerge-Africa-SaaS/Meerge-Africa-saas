from django.urls import include, path
from rest_framework import routers
from .views import AdminStockListView
from .views import AdminStockListApi
from .views import SupplierStockListView
from .views import StockViewApi
from .views import StockDetailViewApi
from .views import SupplierUpdateProfileViewApi
from .inventory_view_api import CreateItemView, CreateStoreView, DeleteStoreByIDView, GetAllStoresByOwnerView, UpdateStoreView, onboardingSupplierView
from .inventory_view_api import ViewStoreDetailByIDView
from .inventory_view_api import CreateStockApiView
from .inventory_view_api import CreateItemCategoryView


from . import api, htmx, views

router = routers.DefaultRouter()
router.register("Category", api.CategoryViewSet)
router.register("Item", api.ItemViewSet)
router.register("Stock", api.StockViewSet)
router.register("Supplier", api.SupplierViewSet)
router.register("SupplyManager", api.SupplyManagerViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path(
        "Category/",
        views.CategoryListView.as_view(),
        name="inventory_Category_list",
    ),
    path(
        "Category/create/",
        views.CategoryCreateView.as_view(),
        name="inventory_Category_create",
    ),
    path(
        "Category/detail/<int:pk>/",
        views.CategoryDetailView.as_view(),
        name="inventory_Category_detail",
    ),
    path(
        "Category/update/<int:pk>/",
        views.CategoryUpdateView.as_view(),
        name="inventory_Category_update",
    ),
    path(
        "Category/delete/<int:pk>/",
        views.CategoryDeleteView.as_view(),
        name="inventory_Category_delete",
    ),
    path(
        "ItemCategory/",
        views.ItemCategoryListView.as_view(),
        name="inventory_ItemCategory_list",
    ),
    path(
        "ItemCategory/create/",
        views.ItemCategoryCreateView.as_view(),
        name="inventory_ItemCategory_create",
    ),
    path(
        "ItemCategory/detail/<int:pk>/",
        views.ItemCategoryDetailView.as_view(),
        name="inventory_ItemCategory_detail",
    ),
    path(
        "ItemCategory/update/<int:pk>/",
        views.ItemCategoryUpdateView.as_view(),
        name="inventory_ItemCategory_update",
    ),
    path(
        "ItemCategory/delete/<int:pk>/",
        views.ItemCategoryDeleteView.as_view(),
        name="inventory_ItemCategory_delete",
    ),
    path("Item/", views.ItemListView.as_view(), name="inventory_Item_list"),
    path(
        "Item/create/",
        views.ItemCreateView.as_view(),
        name="inventory_Item_create",
    ),
    path(
        "Item/detail/<int:pk>/",
        views.ItemDetailView.as_view(),
        name="inventory_Item_detail",
    ),
    path(
        "Item/update/<int:pk>/",
        views.ItemUpdateView.as_view(),
        name="inventory_Item_update",
    ),
    path(
        "Item/delete/<int:pk>/",
        views.ItemDeleteView.as_view(),
        name="inventory_Item_delete",
    ),
   
    path(
        "stock-details/<int:item_id>/",
        StockDetailViewApi.as_view(),
        name="stock-details",
    ),
    path("Stock/", views.StockListView.as_view(), name="inventory_Stock_list"),
    path(
        "Stock/create/", views.StockCreateView.as_view(), name="inventory_Stock_create"
    ),
    path(
        "stock/admin/products/", AdminStockListView.as_view(), name="admin_product_list"
    ),
    path(
        "api/admin/products/",
        AdminStockListApi.as_view(),
        name="admin_api_product_list",
    ),
    path(
        "supplier/<uuid:supplier_id>/products/",
        SupplierStockListView.as_view(),
        name="products_by_supplier",
    ),
    path(
        "Stock/detail/<int:pk>/",
        views.StockDetailView.as_view(),
        name="inventory_Stock_detail",
    ),
    path(
        "Stock/update/<int:pk>/",
        views.StockUpdateView.as_view(),
        name="inventory_Stock_update",
    ),
    path(
        "Stock/delete/<int:pk>/",
        views.StockDeleteView.as_view(),
        name="inventory_Stock_delete",
    ),
    path("Supplier/", views.SupplierListView.as_view(), name="inventory_Supplier_list"),
     path('supplier/profile/update/', SupplierUpdateProfileViewApi.as_view(), name='supplier-update-profile'),
    path(
        "Supplier/create/",
        views.SupplierCreateView.as_view(),
        name="inventory_Supplier_create",
    ),
    path(
        "Supplier/detail/<int:pk>/",
        views.SupplierDetailView.as_view(),
        name="inventory_Supplier_detail",
    ),
    path(
        "Supplier/update/<int:pk>/",
        views.SupplierUpdateView.as_view(),
        name="inventory_Supplier_update",
    ),
    path(
        "Supplier/delete/<int:pk>/",
        views.SupplierDeleteView.as_view(),
        name="inventory_Supplier_delete",
    ),
    path(
        "SupplyManager/",
        views.SupplyManagerListView.as_view(),
        name="inventory_SupplyManager_list",
    ),
    path(
        "SupplyManager/create/",
        views.SupplyManagerCreateView.as_view(),
        name="inventory_SupplyManager_create",
    ),
    path(
        "SupplyManager/detail/<int:pk>/",
        views.SupplyManagerDetailView.as_view(),
        name="inventory_SupplyManager_detail",
    ),
    path(
        "SupplyManager/update/<int:pk>/",
        views.SupplyManagerUpdateView.as_view(),
        name="inventory_SupplyManager_update",
    ),
    path(
        "SupplyManager/delete/<int:pk>/",
        views.SupplyManagerDeleteView.as_view(),
        name="inventory_SupplyManager_delete",
    ),
    path(
        "inventory/htmx/Category/",
        htmx.HTMXCategoryListView.as_view(),
        name="inventory_Category_htmx_list",
    ),
    path(
        "inventory/htmx/Category/create/",
        htmx.HTMXCategoryCreateView.as_view(),
        name="inventory_Category_htmx_create",
    ),
    path(
        "inventory/htmx/Category/delete/<int:pk>/",
        htmx.HTMXCategoryDeleteView.as_view(),
        name="inventory_Category_htmx_delete",
    ),
    path(
        "inventory/htmx/Item/",
        htmx.HTMXItemListView.as_view(),
        name="inventory_Item_htmx_list",
    ),
    path(
        "inventory/htmx/Item/create/",
        htmx.HTMXItemCreateView.as_view(),
        name="inventory_Item_htmx_create",
    ),
    path(
        "inventory/htmx/Item/delete/<int:pk>/",
        htmx.HTMXItemDeleteView.as_view(),
        name="inventory_Item_htmx_delete",
    ),
    path(
        "inventory/htmx/Stock/",
        htmx.HTMXStockListView.as_view(),
        name="inventory_Stock_htmx_list",
    ),
    path(
        "inventory/htmx/Stock/create/",
        htmx.HTMXStockCreateView.as_view(),
        name="inventory_Stock_htmx_create",
    ),
    path(
        "inventory/htmx/Stock/delete/<int:pk>/",
        htmx.HTMXStockDeleteView.as_view(),
        name="inventory_Stock_htmx_delete",
    ),
    path(
        "inventory/htmx/Supplier/",
        htmx.HTMXSupplierListView.as_view(),
        name="inventory_Supplier_htmx_list",
    ),
    path(
        "inventory/htmx/Supplier/create/",
        htmx.HTMXSupplierCreateView.as_view(),
        name="inventory_Supplier_htmx_create",
    ),
    path(
        "inventory/htmx/Supplier/delete/<int:pk>/",
        htmx.HTMXSupplierDeleteView.as_view(),
        name="inventory_Supplier_htmx_delete",
    ),
    path(
        "inventory/htmx/SupplyManager/",
        htmx.HTMXSupplyManagerListView.as_view(),
        name="inventory_SupplyManager_htmx_list",
    ),
    path(
        "inventory/htmx/SupplyManager/create/",
        htmx.HTMXSupplyManagerCreateView.as_view(),
        name="inventory_SupplyManager_htmx_create",
    ),
    path(
        "inventory/htmx/SupplyManager/delete/<int:pk>/",
        htmx.HTMXSupplyManagerDeleteView.as_view(),
        name="inventory_SupplyManager_htmx_delete",
    ),
    path("api/supplier/onboard/", onboardingSupplierView.as_view(), name="create-supplier"),
    path("api/store/create/", CreateStoreView.as_view(), name="create-store"),
    path("api/store/detail/<int:pk>/", ViewStoreDetailByIDView.as_view(), name="view-store-detail-by-id"),
    path("api/stores/all-owner/", GetAllStoresByOwnerView.as_view(), name="get-all-stores-by-owner"),
    path('api/store/delete/<int:pk>/', DeleteStoreByIDView.as_view(), name='store-delete'),
    path('api/stock/create/', CreateStockApiView.as_view(), name='create-stock'),
    path('api/store/update/<int:pk>/', UpdateStoreView.as_view(), name='store-update'),
    path("api/stock-details/", StockViewApi.as_view(), name="product-stock"),
    path('api/item/create/', CreateItemView.as_view(), name='create-item'),
    path('api/item/category/create/', CreateItemCategoryView.as_view(), name='create-item-category'),
   

)