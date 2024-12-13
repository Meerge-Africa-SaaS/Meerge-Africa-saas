from django.urls import include, path
from rest_framework import routers
from .views import AdminStockListView
from .views import AdminStockListApi
from .views import SupplierStockListView
from .views import StockViewApi
from .views import StockDetailViewApi
from .views import SupplierUpdateProfileViewApi
from .views import CreateItemCategoryView
from .views import CreateItemView
from .views import CreateCategoryAndItemView
from .views import CreateItemCategoryView
from .views import ItemSearchAPIView
from .views import DeactivateStockView
from .views import GetItemsByCategoryView
from .views import GetAllStockByCategoryView
from .views import DeleteItemCategoryView
from .views import DeleteItemView
from .views import DeleteStockView
from .views import DeactivateItemView
from .views import ItemCreateAPIView
from .views import GetAllItemsStockBasedOnSupplierCategorieView
from .views import ViewStoreDetailByIDView
from .views import GetAllStoresByOwnerView
from .views import DeleteStoreByIDView
from .views import UpdateStoreView
from .views import CreateStockApiView
from .views import StockDetailView
from .views import UpdateStockView
from .views import UpdateItemCategoryView
from .views import GetAllStocksBySupplierView
from .views import GetAllItemCategoriesView
from .views import GetAllItemsView
from .views import GetItemByIdView
from .views import UpdateItemView
from .views import GetItemsByStockIdView
from .views import GetItemsBySupplierIdView
from .views import CreateItemCategoryView
from .views import ItemCategoryDetailView


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
    path("api/stores/create/", CreateStoreView.as_view(), name="create-store"),
    path("api/item-categories/create/", CreateItemCategoryView.as_view(), name="create-item-category"),
    path("api/items/create/", CreateItemView.as_view(), name="create-item"),
    path("api/item-search/", ItemSearchAPIView.as_view(), name="item-search"),
    path("api/items/by-category/<int:category_id>/", GetItemsByCategoryView.as_view(), name="items-by-category"),
    path("api/stocks/by-category/<int:category_id>/", GetAllStockByCategoryView.as_view(), name="stocks-by-category"),
    path("api/items/by-supplier/<int:supplier_id>/", GetAllItemsStockBasedOnSupplierCategorieView.as_view(), name="items-by-supplier"),
    path("api/stores/by-owner/<int:owner_id>/", GetAllStoresByOwnerView.as_view(), name="stores-by-owner"),
    path("api/stores/delete/<int:pk>/", DeleteStoreByIDView.as_view(), name="delete-store"),
    path("api/stores/update/<int:pk>/", UpdateStoreView.as_view(), name="update-store"),
    path("api/stocks/create/", CreateStockApiView.as_view(), name="create-stock"),
    path("api/stocks/view/", StockViewApi.as_view(), name="view-stock"),
    path("api/stocks/detail/<int:pk>/", StockDetailView.as_view(), name="stock-detail"),
    path("api/stocks/update/<int:pk>/", UpdateStockView.as_view(), name="update-stock"),
    path("api/stocks/delete/<int:pk>/", DeleteStockView.as_view(), name="delete-stock"),
    path("api/items/deactivate/<int:pk>/", DeactivateItemView.as_view(), name="deactivate-item"),
    path("api/stocks/deactivate/<int:pk>/", DeactivateStockView.as_view(), name="deactivate-stock"),
    path("api/items/create/", ItemCreateAPIView.as_view(), name="create-item"),
    path("api/items/by-stock/<int:stock_id>/", GetItemsByStockIdView.as_view(), name="items-by-stock"),
    path("api/items/by-supplier/<int:supplier_id>/", GetItemsBySupplierIdView.as_view(), name="items-by-supplier"),
    path("api/item/updateItemCategory/<int:pk>/", UpdateItemCategoryView.as_view(), name="update-item-category"),
    path("api/item/deleteItemCategory/<int:pk>/", DeleteItemCategoryView.as_view(), name="delete-item-category"),
    path("api/item/getStockCategory/<int:pk>/", GetAllStocksBySupplierView.as_view(), name="get-item-category-by-id"),
    path("api/item/getItemCategory/<int:pk>/", GetAllItemCategoriesView.as_view(), name="get-item-category-by-id"),
    path("api/item/getItems/", GetAllItemsView.as_view(), name="get-items-by-category"),
    path("api/item/getItemById/<int:pk>/", GetItemByIdView.as_view(), name="get-item-by-id"),
    path("api/item/updateItem/<int:pk>/", UpdateItemView.as_view(), name="update-item"),
    path("api/item/deleteItem/<int:pk>/", DeleteItemView.as_view(), name="delete-item"),
    path("api/store/viewStoreDetail/<int:pk>/", ViewStoreDetailByIDView.as_view(), name="view-store-detail"),
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