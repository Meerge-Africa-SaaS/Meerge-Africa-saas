from django.shortcuts import get_object_or_404
from .serializers import  StockSerializer, StoreSerializer, ItemSerializer, ItemCategorySerializer
from .serializers import SupplierSerializer2
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from . import models
from rest_framework.generics import RetrieveAPIView

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