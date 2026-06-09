from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = (
    'id',
    'owner',
    'seller_name',
    'name',
    'description',
    'price',
    'stock',
    'image',
    'created_at'
)

        read_only_fields = (
            'id',
            'owner',
            'seller_name',
            'created_at'
        )