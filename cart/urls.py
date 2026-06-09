from django.urls import path
from .views import CartListCreateView, CartItemDeleteView

urlpatterns = [
    path('', CartListCreateView.as_view()),
    path('<int:pk>/', CartItemDeleteView.as_view()),
]