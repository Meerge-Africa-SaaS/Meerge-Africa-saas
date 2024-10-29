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
from .serializers import ViewStockSerializer
from .serializers import SupplierSerializer
from rest_framework import permissions
from django.http import Http404
from rest_framework.decorators import api_view






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



