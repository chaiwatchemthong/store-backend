from django.urls import path

from .views import OrderListView, CheckoutView

urlpatterns = [
    path('', OrderListView.as_view()),
    path('checkout/', CheckoutView.as_view()),
]