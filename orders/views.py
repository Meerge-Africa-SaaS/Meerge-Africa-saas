from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DeliveryAgent
from .serializers import DeliveryAgentSerializer
from .serializers import CartSerializer
from .models import Cart
from .serializers import CartItemSerializer
from .models import CartItem
from .serializers import AddItemToCartSerializer
from .serializers import RemoveItemFromCartSerializer


from django.dispatch import receiver
''' 
@receiver(delivery_request_created)
def handle_delivery_request_created(sender, instance, created, kwargs):
    if created:
        print("\n"*10, instance, "\n"*10)
 '''


class DeliveryAgentListView(generic.ListView):
    model = models.DeliveryAgent
    form_class = forms.DeliveryAgentForm


class DeliveryAgentCreateView(generic.CreateView):
    model = models.DeliveryAgent
    form_class = forms.DeliveryAgentForm


class DeliveryAgentDetailView(generic.DetailView):
    model = models.DeliveryAgent
    form_class = forms.DeliveryAgentForm


class DeliveryAgentUpdateView(generic.UpdateView):
    model = models.DeliveryAgent
    form_class = forms.DeliveryAgentForm
    pk_url_kwarg = "pk"


class DeliveryAgentDeleteView(generic.DeleteView):
    model = models.DeliveryAgent
    success_url = reverse_lazy("orders_DeliveryAgent_list")

class DeliveryAgentUpdateProfileViewApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        try:
            delivery_agent = DeliveryAgent.objects.get(owner=request.user)
        except DeliveryAgent.DoesNotExist:
            return Response({"error": "Delivery agent profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DeliveryAgentSerializer(delivery_agent, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Check if customer already has a cart
            existing_cart = Cart.objects.get(customer=request.user)
            serializer = CartSerializer(existing_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            # Create new cart if one doesn't exist
            request.data['customer'] = request.user.id
            request.data['created'] = timezone.now()
            serializer = CartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetCustomerCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(customer=request.user)
        except Cart.DoesNotExist:
            # Create new cart if one doesn't exist
            try:
                cart = Cart.objects.create(
                    customer=request.user,
                    product_quantity=0,
                    total_product_price=0,
                    created=timezone.now(),
                )
            except Exception as e:
                return Response(
                    {"error": "Error creating cart", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        try:
            all_cart_items = CartItem.objects.filter(cart=cart)
            
            # Manually construct response data
            response_data = {
                "cart": {
                    "id": str(cart.id),
                    "customer": {
                        "id": cart.customer.id,
                        "username": cart.customer.username,
                        "email": cart.customer.email,
                        "first_name": cart.customer.first_name,
                        "last_name": cart.customer.last_name
                    },
                    "product_quantity": sum(item.product_quantity for item in all_cart_items),
                    "total_price": str(sum(item.total_product_price for item in all_cart_items)),
                    "created_at": cart.created.isoformat()
                },
                "cart_items": [
                    {
                        "id": str(item.id),
                        "item_name": item.item.name,
                        "quantity": item.product_quantity,
                        "price": str(item.total_product_price),
                        "created_at": item.created.isoformat()
                    }
                    for item in all_cart_items
                ]
            }

            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": "Error retrieving cart data", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AddItemToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.get(customer=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                customer=request.user,
                product_quantity=0,
                total_product_price=0,
                created=timezone.now(),
            )
        serializer = CartItemSerializer(data=request.data)
        request.data['cart'] = cart.id
        request.data['customer'] = request.user.id
        request.data['total_product_price'] = request.data['item'].price * request.data['product_quantity']
        request.data['product_quantity'] = request.data['product_quantity']
        request.data['created'] = timezone.now()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveItemFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RemoveItemFromCartSerializer(data=request.data)
        if serializer.is_valid():
            cartItem = CartItem.objects.get(id=request.data['cartItem'])
            cartItem.product_quantity -= request.data['product_quantity']
            cartItem.total_product_price -= request.data['total_product_price']
            if cartItem.product_quantity == 0:
                cartItem.delete()
            cartItem.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
