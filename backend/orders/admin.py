from django.contrib import admin
from orders.models import Cart, Order, OrderItem

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
