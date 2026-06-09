from rest_framework import generics

from .models import CartItem
from .serializers import CartItemSerializer


class CartListCreateView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        item, created = CartItem.objects.get_or_create(
            user=self.request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

class CartItemDeleteView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)