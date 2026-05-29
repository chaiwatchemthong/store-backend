# D:\store\storefront-backend\storefront-backend\products\serializers.py

from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # ดึงชื่อเจ้าของร้านออกมาแสดงผล (Read Only)
    seller_name = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        # 💡 อัปเดตรายชื่อฟิลด์ในทูเพิล (Tuple) ให้เป็นชื่อใหม่ทั้งหมด
        fields = (
            'id', 
            'seller_id', 
            'seller_name', 
            'name',          # เปลี่ยนจาก 'title' -> 'name'
            'description', 
            'price',         # เปลี่ยนจาก 'unit_price' -> 'price'
            'stock',         # เปลี่ยนจาก 'quantity' -> 'stock'
            'image', 
            'created_at'
        )
        # ตั้งค่าช่องที่ระบบคำนวณให้อัตโนมัติ ไม่ต้องส่งมาจากหน้าบ้าน
        read_only_fields = ('id', 'seller_id', 'seller_name', 'created_at')