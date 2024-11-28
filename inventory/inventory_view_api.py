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
# class CreateItemView(APIView):
#     serializer_class = ItemSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         print(request.data,'?*******************************************1')
#         user = request.user
#         print(user,'?*******************************************2')
#         if not user.is_authenticated:
            
#             return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
#         print(user.is_authenticated,'?*******************************************3')
#         # Fetch the supplier based on the authenticated user
#         try:
#             print(user,'?*******************************************4')
#             supplier = models.Supplier.objects.get(owner=user)
#             print(supplier,'?*******************************************5')
#         except models.Supplier.DoesNotExist:
#             print(models.Supplier.DoesNotExist,'?*******************************************6')
#             return Response({'error': 'Supplier account not found'}, status=status.HTTP_404_NOT_FOUND)
#         print(supplier,'?*******************************************7')
#         # Validate and retrieve the category data
#         category_data = request.data.get('category')
#         print(category_data,'?*******************************************8')
#         if isinstance(category_data, dict):
#             print(isinstance(category_data, dict),'?*******************************************9')
#             category_name = category_data.get('name')
#             print(category_name,'?*******************************************10')
#         elif isinstance(category_data, str):
#             print(isinstance(category_data, str),'?*******************************************11')
#             category_name = category_data
#             print(category_name,'?*******************************************12')
#         else:
#             print(category_data,'?*******************************************13')
#             return Response({'error': 'Category data is invalid'}, status=status.HTTP_400_BAD_REQUEST)
#         print(category_name,'?*******************************************14')
#         if not category_name:
#             print(not category_name,'?*******************************************15')
#             return Response({'error': 'Category name is required'}, status=status.HTTP_400_BAD_REQUEST)
#         print(category_name,'?*******************************************16')
#         # Fetch the category based on the name
#         try:
#             print(category_name,'?*******************************************17')
#             category = models.ItemCategory.objects.get(name=category_name)
#             print(category,'?*******************************************18')
#         except models.ItemCategory.DoesNotExist:
#             print(models.ItemCategory.DoesNotExist,'?*******************************************19')
#             return Response({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         print(category,'?*******************************************20')
#         # Ensure the item data exists and is a dictionary
#         item_data = request.data
#         print(item_data,'?*******************************************21')
#         if not item_data or not isinstance(item_data, dict):
#             print(not item_data or not isinstance(item_data, dict),'?*******************************************22')
#             return Response({'error': 'Invalid item data format'}, status=status.HTTP_400_BAD_REQUEST)

#         # Ensure the item name exists
#         item_name = item_data.get('name')
#         print(item_name,'?*******************************************23')
#         # Check if the supplier already has an item with the same name and category
#         existing_item = models.Item.objects.filter(
#             name=item_name,
#             category=category,
#             supplier=supplier
#         ).first()
#         print(existing_item,'?*******************************************24')
#         if existing_item:
#             return Response({'error': 'You already have an item with this name and category'}, status=status.HTTP_400_BAD_REQUEST)
#         print(existing_item,'?*******************************************25')
#         # Add the supplier to item data before saving
#         item_data['supplier'] = supplier.id
#         print(item_data,'?*******************************************26')
#         serializer = self.serializer_class(data=item_data)
#         print(serializer,'?*******************************************27')
#         if serializer.is_valid():
#             print(serializer.is_valid(),'?*******************************************28')
#             print(serializer," <<<<<<<< this is the item data before saving.============================================. 29")
#             item = serializer.save()
#             print(item,'?*******************************************29')
#             return Response({'message': 'Item created successfully', 'item': serializer.data}, status=status.HTTP_201_CREATED)
#         print(serializer.errors,'?*******************************************30')
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
        print(f"User details: {user.__dict__}")
        print(request.data,'<<<<<<?*******************************************1')
        serializer = self.serializer_class(data=request.data)
        print(serializer,'?*******************************************2')
        if serializer.is_valid():
            print(serializer.is_valid(),'?*******************************************3')
            serializer.validated_data['owner'] = request.user
            print(serializer.validated_data,'?*******************************************4')
            supplier = serializer.save()
            print(supplier,'?*******************************************5')
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
        print(request.data,'?*******************************************1')
        serializer = self.serializer_class(data=request.data)
        print(serializer,'?*******************************************2')
        if serializer.is_valid():
            print(serializer.is_valid(),'?*******************************************3')
            serializer.save()
            print(serializer.data,'?*******************************************4')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)