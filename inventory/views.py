from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Item, Stock, Supplier
from .serializers import StockSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from .serializers import AdminViewAllProductSerializer
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Store
from .serializers import StoreSerializer
from .serializers import CategorySerializer
from .serializers import ItemSerializer
from .serializers import ViewStockSerializer
from .serializers import SupplierSerializer
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .serializers import  StockSerializer, StoreSerializer, ItemSerializer, ItemCategorySerializer
from .serializers import SupplierSerializer2
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from . import models
from rest_framework.generics import RetrieveAPIView







from . import forms, models


class CategoryListView(generic.ListView):
    model = models.Category
    form_class = forms.CategoryForm


class CategoryCreateView(generic.CreateView):
    model = models.Category
    form_class = forms.CategoryForm


class CategoryDetailView(generic.DetailView):
    model = models.Category
    form_class = forms.CategoryForm


class CategoryUpdateView(generic.UpdateView):
    model = models.Category
    form_class = forms.CategoryForm
    pk_url_kwarg = "pk"


class CategoryDeleteView(generic.DeleteView):
    model = models.Category
    success_url = reverse_lazy("inventory_Category_list")


class ItemCategoryListView(generic.ListView):
    model = models.ItemCategory
    form_class = forms.ItemCategoryForm


class ItemCategoryCreateView(generic.CreateView):
    model = models.ItemCategory
    form_class = forms.ItemCategoryForm


class ItemCategoryDetailView(generic.DetailView):
    model = models.ItemCategory
    form_class = forms.ItemCategoryForm


class ItemCategoryUpdateView(generic.UpdateView):
    model = models.ItemCategory
    form_class = forms.ItemCategoryForm
    pk_url_kwarg = "pk"


class ItemCategoryDeleteView(generic.DeleteView):
    model = models.ItemCategory
    success_url = reverse_lazy("inventory_ItemCategory_list")



class ItemListView(generic.ListView):
    model = models.Item
    form_class = forms.ItemForm


class ItemCreateView(generic.CreateView):
    model = models.Item
    form_class = forms.ItemForm


class ItemDetailView(generic.DetailView):
    model = models.Item
    form_class = forms.ItemForm


class ItemUpdateView(generic.UpdateView):
    model = models.Item
    form_class = forms.ItemForm
    pk_url_kwarg = "pk"


class ItemDeleteView(generic.DeleteView):
    model = models.Item
    success_url = reverse_lazy("inventory_Item_list")

class AdminStockListApi(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'User is not logged in'}, status=401)
        
        products = Stock.objects.all()
        serializer = StockSerializer(products, many=True)
        return Response(serializer.data)
class AdminStockListView(APIView):
   

    def get(self, request):
        products = Stock.objects.all()  
        serializer = AdminViewAllProductSerializer(products, many=True)
        return Response(serializer.data)

    def admin_product_list_view(request):
        if request.user.is_authenticated and request.user.is_staff:
            products = Stock.objects.all()
            return render(request, 'stock_admin_list.html', {'products': products})
        else:
            return render(request, '403.html')


    
class SupplierStockListView(APIView):
    
    def get(self, request, supplier_id):
        supplier = get_object_or_404(Supplier, id=supplier_id)
        items = Item.objects.filter(supplier=supplier).prefetch_related('stock_set')
        product_details = []
        for item in items:
            stocks = item.stock_set.all()
            for stock in stocks:
                product_details.append({
                    'product_name': item.name,
                    'product_image': stock.product_image.url if stock.product_image else None,
                    'product_category': item.category.name if item.category else None,
                    'price': item.price,
                    'units_available': stock.unit_available if stock.unit_available else 0,
                    'discount_percentage': stock.discount_percentage if stock.discount_percentage else None,
                    'size': stock.size if stock.size else None,
                })

        data = {
            'products': product_details,
            'supplier_name': supplier.name, 
        }
        return Response(data)
class StockListView(generic.ListView):
    model = models.Stock
    form_class = forms.StockForm

class StockCreateView(generic.CreateView):
    model = models.Stock
    form_class = forms.StockForm


class StockCreateAPIView(generics.CreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            stock = serializer.save()
            return Response(
                {"id": stock.id, "message": "Stock created successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockViewApi(generics.ListAPIView):
    queryset = models.Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
    
class StockDetailView(generic.DetailView):
    model = models.Stock
    form_class = forms.StockForm


class StockUpdateView(generic.UpdateView):
    model = models.Stock
    form_class = forms.StockForm
    pk_url_kwarg = "pk"


class StockDeleteView(generic.DeleteView):
    model = models.Stock
    success_url = reverse_lazy("inventory_Stock_list")


class SupplierListView(generic.ListView):
    model = models.Supplier
    form_class = forms.ViewSupplierForm
    

class SupplierCreateView(generic.TemplateView):
    model = models.Supplier
    form_class = forms.SupplierForm
    template_name = "inventory/supplier_registration/base.html"


class SupplierDetailView(generic.DetailView):
    model = models.Supplier
    form_class = forms.ViewSupplierForm

class SupplierProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            supplier = Supplier.objects.get(owner=request.user)
        except Supplier.DoesNotExist:
            return Response({"error": "Supplier profile not found."}, status=status.HTTP_404_NOT_FOUND)
        profile_data = {
            "business_logo": request.build_absolute_uri(supplier.profile_img.url) if supplier.profile_img else None,
            "business_cover_image": request.build_absolute_uri(supplier.cover_img.url) if supplier.cover_img else None,
            "business_category": supplier.category,
            "food_business_license": request.build_absolute_uri(supplier.business_license.url) if supplier.business_license else None,
            "email": supplier.email,
            "phone_number": supplier.phone_number,
            "business_email": supplier.email,
            "business_phone_number": supplier.phone_number, 
            "business_address": supplier.address,
            "business_video_upload": None, 
        }

        return Response(profile_data, status=status.HTTP_200_OK)



class SupplierUpdateProfileViewApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SupplierSerializer

    def put(self, request):
        try:
            supplier = Supplier.objects.get(owner=request.user)
        except Supplier.DoesNotExist:
            return Response({"error": "Supplier profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SupplierSerializer(supplier, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SupplierUpdateView(generic.UpdateView):
    model = models.Supplier
    form_class = forms.SupplierForm
    pk_url_kwarg = "pk"


class SupplierDeleteView(generic.DeleteView):
    model = models.Supplier
    success_url = reverse_lazy("inventory_Supplier_list")


class SupplyManagerListView(generic.ListView):
    model = models.SupplyManager
    form_class = forms.SupplyManagerForm


class SupplyManagerCreateView(generic.CreateView):
    model = models.SupplyManager
    form_class = forms.SupplyManagerForm


class SupplyManagerDetailView(generic.DetailView):
    model = models.SupplyManager
    form_class = forms.SupplyManagerForm


class SupplyManagerUpdateView(generic.UpdateView):
    model = models.SupplyManager
    form_class = forms.SupplyManagerForm
    pk_url_kwarg = "pk"


class SupplyManagerDeleteView(generic.DeleteView):
    model = models.SupplyManager
    success_url = reverse_lazy("inventory_SupplyManager_list")

class CreateStoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StoreSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateCategoryAndItemView(APIView):
    def post(self, request):
        category_name = request.data.get('category', {}).get('name')
        if not category_name:
            return Response({'error': 'Category name is required'}, status=status.HTTP_400_BAD_REQUEST)
        category, _ = models.Category.objects.get_or_create(name=category_name)
        item_data = request.data.get('item')
        if not item_data or not item_data.get('name'):
            return Response({'error': 'Item name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        item_name = item_data.get('name')
        item = Item.objects.filter(name=item_name, category=category).first()
        
        if item:
            stock = Stock.objects.filter(item=item).first()
            if stock:
                stock.quantity += item_data.get('quantity', 0)
                stock.save()
                return Response({
                    'message': 'Stock quantity updated.',
                    'category': CategorySerializer(category).data,
                    'item': ItemSerializer(item).data,
                    'stock': StockSerializer(stock).data
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'New stock created for existing item.',
                'category': CategorySerializer(category).data,
                'item': ItemSerializer(item).data,
                'stock': StockSerializer(stock).data
            }, status=status.HTTP_201_CREATED)
        else:
            item_data['category'] = category.id  
            item_serializer = ItemSerializer(data=item_data)
            if item_serializer.is_valid():
                item = item_serializer.save()
                stock = Stock.objects.create(
                    item=item,
                    quantity=item_data.get('quantity', 0),
                    product_image=item_data.get('product_image')
                )
                return Response({
                    'message': 'New item and stock created.',
                    'category': CategorySerializer(category).data,
                    'item': ItemSerializer(item).data,
                    'stock': StockSerializer(stock).data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class StockDetailViewApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        user = request.user
        item = get_object_or_404(Item, id=item_id, supplier=user)
        stock = get_object_or_404(Stock, item=item)
        low_stock_alert = stock.quantity < 5

        stock_data = ViewStockSerializer(stock).data
        stock_data['low_stock_alert'] = low_stock_alert
        return Response(stock_data)


# class CreateCategoryAndItemView(APIView):
#     def post(self, request):
#         # Step 1: Get the category name from the request data
#         category_name = request.data.get('category', {}).get('name')
#         if not category_name:
#             return Response({'error': 'Category name is required'}, status=status.HTTP_400_BAD_REQUEST)

#         # Step 2: Get or create the category based on the provided name
#         category, _ = models.Category.objects.get_or_create(name=category_name)

#         # Step 3: Get the item data from the request data
#         item_data = request.data.get('item')
#         if not item_data or not item_data.get('name'):
#             return Response({'error': 'Item name is required'}, status=status.HTTP_400_BAD_REQUEST)

#         item_name = item_data.get('name')

#         # Step 4: Check if the item exists within the given category
#         item = Item.objects.filter(name=item_name, category=category).first()

#         if item:
#             # Step 5: If item exists, check if stock exists for the item
#             stock = Stock.objects.filter(item=item).first()
#             if stock:
#                 # Step 6: If stock exists, update the stock quantity
#                 stock.quantity += item_data.get('quantity', 0)
#                 stock.save()
#                 return Response({
#                     'message': 'Stock quantity updated.',
#                     'category': CategorySerializer(category).data,
#                     'item': ItemSerializer(item).data,
#                     'stock': StockSerializer(stock).data
#                 }, status=status.HTTP_200_OK)

#             else:
#                 # Step 7: If item exists but no stock, create new stock for the item
#                 stock = Stock.objects.create(
#                     item=item,  # Linking the item to stock
#                     quantity=item_data.get('quantity', 0),  # Set quantity, defaulting to 0 if not provided
#                     product_image=item_data.get('product_image'),  # Use product image from the request
#                     SKU_No=item_data.get('SKU_No', ''),  # Optional SKU, default to empty string
#                     Product_Name=item_data.get('Product_Name', item.name),  # Default to item name if not provided
#                     Product_Category=item_data.get('Product_Category', category.name),  # Default to category name
#                     Manufacturer_Name=item_data.get('Manufacturer_Name', ''),  # Optional, default to empty string
#                     Price=item_data.get('Price', 0.00),  # Optional, default to 0.00
#                     Units_Available=item_data.get('Units_Available', 0),  # Optional, default to 0
#                     Size=item_data.get('Size', ''),  # Optional, default to empty string
#                     Weight=item_data.get('Weight', ''),  # Optional, default to empty string
#                     Availability_Status=item_data.get('Availability_Status', 'In Stock'),  # Optional, default status
#                     Discount_Percentage=item_data.get('Discount_Percentage', 0.00),  # Optional, default to 0%
#                     Delivery_Time_Estimate=item_data.get('Delivery_Time_Estimate', ''),  # Optional, default to empty string
#                     Pickup_Option=item_data.get('Pickup_Option', 'No Pickup'),  # Optional, default to 'No Pickup'
#                     Password=item_data.get('Password', '')  # Optional, default to empty string
#                 )
#                 return Response({
#                     'message': 'New stock created for existing item.',
#                     'category': CategorySerializer(category).data,
#                     'item': ItemSerializer(item).data,
#                     'stock': StockSerializer(stock).data
#                 }, status=status.HTTP_201_CREATED)
        
#         else:
#             # Step 8: If the item doesn't exist, create a new item and stock
#             item_data['category'] = category.id
#             item_serializer = ItemSerializer(data=item_data)
#             if item_serializer.is_valid():
#                 item = item_serializer.save()
                
#                 # Create the stock for the new item
#                 stock = Stock.objects.create(
#                     item=item,
#                     quantity=item_data.get('quantity', 0),
#                     product_image=item_data.get('product_image')
#                 )
#                 return Response({
#                     'message': 'New item and stock created.',
#                     'category': CategorySerializer(category).data,
#                     'item': ItemSerializer(item).data,
#                     'stock': StockSerializer(stock).data
#                 }, status=status.HTTP_201_CREATED)
#             else:
#                 # Step 9: Handle invalid item serializer data
#                 return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeactivateStockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, stock_id):
        try:
            # Get the stock object by ID
            stock = get_object_or_404(Stock, id=stock_id)

            # Deactivate the stock
            stock.is_active = False
            stock.save()

            # Get all items associated with this stock and deactivate them
            items = Item.objects.filter(stock=stock)
            deactivated_items = []
            for item in items:
                item.is_active = False
                item.save()
                deactivated_items.append({
                    'id': item.id,
                    'name': item.name,
                    'is_active': False
                })

            return Response({
                'message': 'Stock and associated items deactivated successfully',
                'stock': {
                    'id': stock.id,
                    'is_active': False
                },
                'deactivated_items': deactivated_items
            }, status=status.HTTP_200_OK)

        except Stock.DoesNotExist:
            return Response({
                'error': f'Stock with ID {stock_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': f'Error deactivating stock: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeactivateItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        item.is_active = False
        item.save()
        return Response({"message": "Item deactivated successfully"}, status=status.HTTP_200_OK)



class ItemCreateAPIView(generics.CreateAPIView):
    queryset = models.Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Get category from request data
        category_id = request.data.get('category')
        try:
            category = models.Category.objects.get(id=category_id)
        except models.Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add supplier info if authenticated user is a supplier
        try:
            supplier = Supplier.objects.get(owner=request.user)
            request.data['supplier'] = supplier.id
        except Supplier.DoesNotExist:
            return Response(
                {"error": "User is not registered as a supplier"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            return Response({
                "message": "Item created successfully",
                "data": ItemSerializer(item).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ItemSearchAPIView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.Item.objects.all()
        search_term = self.request.query_params.get('search', None)
        
        if search_term:
            # Using icontains for case-insensitive partial matching
            queryset = queryset.filter(name__icontains=search_term)
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"message": "No items found matching your search"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Items found",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

class GetAllItemsStockBasedOnSupplierCategorieView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            supplier = Supplier.objects.get(owner=request.user)
            supplier_categories = supplier.category.all()
            items = Item.objects.filter(category__in=supplier_categories)
            serializer = ItemSerializer(items, many=True)
            
            return Response({
                "message": "Items retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Supplier.DoesNotExist:
            return Response({
                "error": "User is not registered as a supplier"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ========================================================================================
# STORE VIEWS 🏬🏬🏪🏪
# ========================================================================================
class CreateStoreView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StoreSerializer

    def post(self, request):
        data = request.data.copy()
        data['store_owner'] = request.user.id

        serializer = StoreSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewStoreDetailByIDView(RetrieveAPIView):
    queryset = models.Store.objects.all()  
    serializer_class = StoreSerializer  
    permission_classes = [IsAuthenticated] 


class GetAllStoresByOwnerView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StoreSerializer

    def get(self, request):
        stores = models.Store.objects.filter(store_owner=request.user)
        serializer = self.serializer_class(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class DeleteStoreByIDView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        store = get_object_or_404(models.Store, pk=pk, store_owner=request.user)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class UpdateStoreView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StoreSerializer

    def put(self, request, pk):
        try:
            store = models.Store.objects.get(pk=pk, store_owner=request.user)
        except models.Store.DoesNotExist:
            return Response({"error": "Store not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(store, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# ========================================================================================
# STOCK VIEWS  🛒🛒🛒🛒
# ========================================================================================

class CreateStockApiView(APIView):
    queryset = models.Stock.objects.all()
    serializer_class = StockSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            stock = serializer.save()
            return Response(
                {"id": stock.id, "message": "Stock created successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class StockViewApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get all stocks
            stocks = models.Stock.objects.all()
            serializer = StockSerializer(stocks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Error retrieving stocks", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StockDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            # Get stock by ID
            stock = get_object_or_404(models.Stock, pk=pk)
            serializer = StockSerializer(stock)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Stock.DoesNotExist:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Error retrieving stock", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateStockView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer

    def put(self, request, pk):
        try:
            stock = get_object_or_404(models.Stock, pk=pk)
            serializer = self.serializer_class(stock, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Stock.DoesNotExist:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Error updating stock", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteStockView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            stock = get_object_or_404(models.Stock, pk=pk)
            stock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Stock.DoesNotExist:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Error deleting stock", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class GetAllStocksBySupplierView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer

    def get(self, request, supplier_id):
        try:
            # Verify supplier exists
            supplier = get_object_or_404(models.Supplier, id=supplier_id)
            
            # Get all stocks for this supplier
            stocks = models.Stock.objects.filter(supplier=supplier)
            
            # Serialize the stocks
            serializer = self.serializer_class(stocks, many=True)
            
            return Response({
                "message": "Stocks retrieved successfully",
                "supplier": supplier.name,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except models.Supplier.DoesNotExist:
            return Response({
                "error": "Supplier not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                "error": "Error retrieving stocks",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetAllStockByCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer

    def get(self, request, category_id):
        try:
            # Verify category exists
            category = get_object_or_404(models.ItemCategory, id=category_id)
            
            # Get all stocks for this category
            stocks = models.Stock.objects.filter(category=category)
            
            # Serialize the stocks
            serializer = self.serializer_class(stocks, many=True)
            
            return Response({
                "message": "Stocks retrieved successfully",
                "category": category.name,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except models.ItemCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


# ========================================================================================
# Item VIEWS 🍔🍔🍔🍔
# ========================================================================================


class CreateItemView(APIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            supplier = models.Supplier.objects.get(owner=user)
        except models.Supplier.DoesNotExist:
            return Response({'error': 'Supplier account not found'}, status=status.HTTP_404_NOT_FOUND)

        # Validate category data
        category_data = request.data.get('category')
        if isinstance(category_data, dict):
            category_name = category_data.get('name')
        elif isinstance(category_data, str):
            category_name = category_data
        else:
            return Response({'error': 'Category data is invalid'}, status=status.HTTP_400_BAD_REQUEST)

        if not category_name:
            return Response({'error': 'Category name is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = models.ItemCategory.objects.get(name=category_name)
        except models.ItemCategory.DoesNotExist:
            return Response({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)

        item_data = request.data
        item_data['supplier'] = supplier  # Add supplier to item_data
        item_data['category'] = category    # Add category directly

        serializer = self.serializer_class(data=item_data)
        if serializer.is_valid():
            item = serializer.save()
            return Response({'message': 'Item created successfully', 'item': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetAllItemsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get(self, request):
        items = models.Item.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetItemByIdView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get(self, request, item_id):
        try:
            item = models.Item.objects.get(id=item_id)
            serializer = self.serializer_class(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Item.DoesNotExist:
            return Response(
                {"error": "Item not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class UpdateItemView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def put(self, request, item_id):
        try:
            item = models.Item.objects.get(id=item_id)
            
            # Check if user is the supplier who created the item
            if item.stock and item.stock.supplier.owner != request.user:
                return Response(
                    {"error": "Not authorized to update this item"},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            serializer = self.serializer_class(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except models.Item.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class DeleteItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = models.Item.objects.get(id=item_id)
            
            # Check if user is the supplier who created the item
            if item.stock and item.stock.supplier.owner != request.user:
                return Response(
                    {"error": "Not authorized to delete this item"},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except models.Item.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class GetItemsByStockIdView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get(self, request, stock_id):
        try:
            items = models.Item.objects.filter(stock_id=stock_id)
            serializer = self.serializer_class(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetItemsBySupplierIdView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get(self, request, supplier_id):
        try:
            items = models.Item.objects.filter(stock__supplier_id=supplier_id)
            serializer = self.serializer_class(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetItemsByCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get(self, request, category_id):
        try:
            # Verify category exists
            category = get_object_or_404(models.ItemCategory, id=category_id)
            
            # Get all items for this category
            items = models.Item.objects.filter(category=category)
            
            # Serialize the items
            serializer = self.serializer_class(items, many=True)
            
            return Response({
                "message": "Items retrieved successfully",
                "category": category.name,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except models.ItemCategory.DoesNotExist:
            return Response({
                "error": "Category not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                "error": "Error retrieving items",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ========================================================================================
# Supplier VIEWS 👩‍🌾👩‍🌾👩‍🌾👩‍🌾
# ========================================================================================

class onboardingSupplierView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierSerializer2

    def post(self, request):
        # Log the logged-in user details
        user = request.user
        print(f"Logged-in user: ID={user.id}, Username={user.username}, Email={user.email}")
        
        # If you want more detailed information, you can add more fields:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            supplier = serializer.save()
            return Response({
                'message': 'Supplier created successfully',
                'supplier': SupplierSerializer2(supplier).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




# ========================================================================================
# Item Categories 👩‍🌾👩‍🌾👩‍🌾👩‍🌾
# ========================================================================================
class CreateItemCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemCategorySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllItemCategoriesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemCategorySerializer

    def get(self, request):
        try:
            categories = models.ItemCategory.objects.all()
            serializer = self.serializer_class(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Error retrieving categories", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ItemCategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemCategorySerializer

    def get(self, request, pk):
        try:
            category = get_object_or_404(models.ItemCategory, pk=pk)
            serializer = self.serializer_class(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.ItemCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Error retrieving category", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateItemCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemCategorySerializer

    def put(self, request, pk):
        try:
            category = get_object_or_404(models.ItemCategory, pk=pk)
            serializer = self.serializer_class(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.ItemCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Error updating category", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteItemCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            category = get_object_or_404(models.ItemCategory, pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.ItemCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Error deleting category", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetItemsByCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get(self, request, category_id):
        try:
            items = models.Item.objects.filter(category_id=category_id)
            serializer = self.serializer_class(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Error retrieving items please try again", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )