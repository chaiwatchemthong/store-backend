from django.urls import path
from . import views

urlpatterns = [
    # 1. เส้นทางสำหรับการสมัครสมาชิก (Register) -> ชี้ไปที่ฟังก์ชัน def register(request)
    path('register/', views.register, name='register'),
    
    # 2. เส้นทางสำหรับการเข้าสู่ระบบ (Login) -> ชี้ไปที่ฟังก์ชัน def login(request)
    path('login/', views.login, name='login'),
    
    # 3. เส้นทางสำหรับดึงข้อมูลโปรไฟล์ของตัวเอง (Me) -> ชี้ไปที่ฟังก์ชัน def me(request)
    path('me/', views.me, name='me'),
]