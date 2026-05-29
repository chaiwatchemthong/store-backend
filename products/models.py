# products/models.py
from django.db import models
from django.conf import settings

class Product(models.Model):
    # เชื่อมโยงกับผู้ใช้งาน (ใครเป็นคนลงขายสินค้าชิ้นนี้)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name