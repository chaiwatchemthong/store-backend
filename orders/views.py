from decimal import Decimal

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderItem
from .serializers import OrderSerializer

from cart.models import CartItem


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


class CheckoutView(APIView):

    def post(self, request):
        cart_items = CartItem.objects.filter(
            user=request.user
        )

        if not cart_items.exists():
            return Response(
                {'detail': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = Decimal('0.00')

        order = Order.objects.create(
            user=request.user
        )

        for item in cart_items:

            subtotal = item.product.price * item.quantity

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            total += subtotal

            # ตัดสต็อกสินค้า
            item.product.stock -= item.quantity
            item.product.save()

        order.total_price = total
        order.status = 'completed'
        order.save()

        # ล้างตะกร้า
        cart_items.delete()

        return Response(
            OrderSerializer(order).data
        )