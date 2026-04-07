from django.contrib.auth.models import User
from rest_framework import serializers

from menu.models import MenuItem
from orders.models import Cart, Order, OrderItem


class MenuItemShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price']


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemShortSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Cart
        fields = ['id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
        read_only_fields = ['id', 'unit_price', 'price', 'menuitem']


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemShortSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='order_items', many=True, read_only=True)
    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'items']
        read_only_fields = ['id', 'user', 'total', 'date', 'items']

    def validate_status(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError('Status must be 0 or 1.')
        return value
