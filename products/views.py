# D:\store\storefront-backend\storefront-backend\products\views.py

from rest_framework.generics import ListCreateAPIView, ListAPIView
# 💡 จุดสำคัญ: ต้อง Import สิทธิ์ IsAuthenticated เข้ามาบรรทัดนี้เพื่อไม่ให้ขึ้น Error ครับ
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # ล็อกระบบให้เฉพาะผู้ใช้ที่เข้าสู่ระบบ (Login) แล้วเท่านั้น ถึงจะเพิ่มสินค้าได้
    permission_classes = [IsAuthenticated] 

    # 💡 แก้ไขบรรทัดที่พิมพ์ซ้อนกัน ให้แยกออกมาเขียนแบบนี้ครับ
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyProductsView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ดึงมาแสดงผลเฉพาะสินค้าที่ผู้ใช้คนนี้ (Seller) เป็นเจ้าของ
        return Product.objects.filter(owner=self.request.user)