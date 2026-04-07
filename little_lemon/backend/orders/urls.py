from django.urls import path

from orders.views import CartMenuItemsView, OrdersView, SingleOrderView

urlpatterns = [
    path('cart/menu-items', CartMenuItemsView.as_view()),
    path('orders', OrdersView.as_view()),
    path('orders/<int:pk>', SingleOrderView.as_view()),
]
