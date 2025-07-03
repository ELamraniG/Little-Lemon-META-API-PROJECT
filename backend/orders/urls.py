from django.urls import path

from orders.views import CartView, OrdersView, OrdersIdView

urlpatterns = [
    path('cart/menu-items', CartView.as_view()),
    path('orders', OrdersView.as_view()),
    path('orders/<int:pk>', OrdersIdView.as_view()),
]
