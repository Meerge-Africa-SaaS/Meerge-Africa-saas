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
