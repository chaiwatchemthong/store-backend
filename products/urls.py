# products/urls.py
from django.urls import path
from . import views  # 👈 เช็กตรงนี้ว่าอิมพอร์ต views มาถูกไหม

urlpatterns = [
    # หน้าแรกของโปรดักส์ดักรับทั้ง GET และ POST
    path('', views.ProductListCreateView.as_view(), name='product-list-create'),
    
    # หน้าสินค้าของฉัน
    path('my/', views.MyProductsView.as_view(), name='my-products'),
]