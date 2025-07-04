from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.models import MenuItem
from orders.models import Cart, Order, OrderItem
from orders.serializers import CartSerializer, OrderSerializer
from users.permissions import isDeliveryCrew, isManager


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cartItems = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cartItems, many=True)
        return Response(serializer.data)

    def post(self, request):
        menuItemId = request.data.get('menuitem_id')
        quantity = int(request.data.get('quantity', 1))

        if quantity < 1:
            return Response({'message': 'Quantity must be 1 or more.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            menuItem = MenuItem.objects.get(id=menuItemId)
        except MenuItem.DoesNotExist:
            return Response({'message': 'Menu item not found.'}, status=status.HTTP_404_NOT_FOUND)

        unitPrice = menuItem.price
        price = unitPrice * quantity
        cartItem, created = Cart.objects.get_or_create(
            user=request.user,
            menuitem=menuItem,
            defaults={'quantity': quantity, 'unit_price': unitPrice, 'price': price},
        )

        if not created:
            cartItem.quantity = quantity
            cartItem.unit_price = unitPrice
            cartItem.price = price
            cartItem.save()

        serializer = CartSerializer(cartItem)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({'message': 'Cart cleared.'}, status=status.HTTP_200_OK)


class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if isManager(request.user):
            orders = Order.objects.all()
        elif isDeliveryCrew(request.user):
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(user=request.user)

        orders = orders.order_by('-date', '-id')
        paginator = PageNumberPagination()
        paginator.page_size_query_param = 'perpage'
        page = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @transaction.atomic
    def post(self, request):
        cartItems = Cart.objects.filter(user=request.user)
        if not cartItems.exists():
            return Response({'message': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user, total=0, date=timezone.localdate())
        total = 0

        for cartItem in cartItems:
            OrderItem.objects.create(
                order=order,
                menuitem=cartItem.menuitem,
                quantity=cartItem.quantity,
                unit_price=cartItem.unit_price,
                price=cartItem.price,
            )
            total += cartItem.price

        order.total = total
        order.save()
        cartItems.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrdersIdView(APIView):
    permission_classes = [IsAuthenticated]

    def getOrderById(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.getOrderById(pk)
        if order is None:
            return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        return self.updateOrder(request, pk, partial=False)

    def patch(self, request, pk):
        return self.updateOrder(request, pk, partial=True)

    def updateOrder(self, request, pk, partial):
        order = self.getOrderById(pk)
        if order is None:
            return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if isManager(request.user):
            data = {
                'delivery_crew': request.data.get('delivery_crew', order.delivery_crew_id),
                'status': request.data.get('status', order.status),
            }

            deliveryCrewId = data.get('delivery_crew')
            if deliveryCrewId is not None:
                try:
                    deliveryCrew = User.objects.get(id=deliveryCrewId)
                except User.DoesNotExist:
                    return Response({'message': 'Delivery crew user not found.'}, status=status.HTTP_400_BAD_REQUEST)

                if not deliveryCrew.groups.filter(name='Delivery crew').exists():
                    return Response({'message': 'User is not in Delivery crew group.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = OrderSerializer(order, data=data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if isDeliveryCrew(request.user):
            if order.delivery_crew_id != request.user.id:
                return Response({'message': 'You can only update assigned orders.'}, status=status.HTTP_403_FORBIDDEN)

            if 'status' not in request.data:
                return Response({'message': 'Only status can be updated.'}, status=status.HTTP_400_BAD_REQUEST)

            orderStatus = request.data.get('status')
            if orderStatus not in [0, 1, '0', '1']:
                return Response({'message': 'Status must be 0 or 1.'}, status=status.HTTP_400_BAD_REQUEST)

            order.status = int(orderStatus)
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)

        return Response({'message': 'Not allowed to update this order.'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        order = self.getOrderById(pk)
        if order is None:
            return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not isManager(request.user):
            return Response({'message': 'Only managers can delete orders.'}, status=status.HTTP_403_FORBIDDEN)

        order.delete()
        return Response({'message': 'Order deleted.'}, status=status.HTTP_200_OK)
