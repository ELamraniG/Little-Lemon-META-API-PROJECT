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
from users.permissions import user_is_delivery_crew, user_is_manager


class CartMenuItemsView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		items = Cart.objects.filter(user=request.user)
		serializer = CartSerializer(items, many=True)
		return Response(serializer.data)

	def post(self, request):
		menuitem_id = request.data.get('menuitem_id')
		quantity = int(request.data.get('quantity', 1))

		if quantity < 1:
			return Response({'message': 'Quantity must be 1 or more.'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			menu_item = MenuItem.objects.get(id=menuitem_id)
		except MenuItem.DoesNotExist:
			return Response({'message': 'Menu item not found.'}, status=status.HTTP_404_NOT_FOUND)

		unit_price = menu_item.price
		total_price = unit_price * quantity
		cart_item, created = Cart.objects.get_or_create(
			user=request.user,
			menuitem=menu_item,
			defaults={'quantity': quantity, 'unit_price': unit_price, 'price': total_price},
		)

		if not created:
			cart_item.quantity = quantity
			cart_item.unit_price = unit_price
			cart_item.price = total_price
			cart_item.save()

		serializer = CartSerializer(cart_item)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def delete(self, request):
		Cart.objects.filter(user=request.user).delete()
		return Response({'message': 'Cart cleared.'}, status=status.HTTP_200_OK)


class OrdersView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		if user_is_manager(request.user):
			order_list = Order.objects.all()
		elif user_is_delivery_crew(request.user):
			order_list = Order.objects.filter(delivery_crew=request.user)
		else:
			order_list = Order.objects.filter(user=request.user)

		order_list = order_list.order_by('-date', '-id')
		paginator = PageNumberPagination()
		paginator.page_size_query_param = 'perpage'
		page = paginator.paginate_queryset(order_list, request)
		serializer = OrderSerializer(page, many=True)
		return paginator.get_paginated_response(serializer.data)

	@transaction.atomic
	def post(self, request):
		cart_items = Cart.objects.filter(user=request.user)
		if not cart_items.exists():
			return Response({'message': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

		order = Order.objects.create(user=request.user, total=0, date=timezone.localdate())
		total = 0

		for item in cart_items:
			OrderItem.objects.create(
				order=order,
				menuitem=item.menuitem,
				quantity=item.quantity,
				unit_price=item.unit_price,
				price=item.price,
			)
			total += item.price

		order.total = total
		order.save()
		cart_items.delete()

		serializer = OrderSerializer(order)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleOrderView(APIView):
	permission_classes = [IsAuthenticated]

	def get_object(self, pk):
		try:
			return Order.objects.get(pk=pk)
		except Order.DoesNotExist:
			return None

	def can_view_order(self, user, order):
		if user_is_manager(user):
			return True
		if user_is_delivery_crew(user):
			return order.delivery_crew_id == user.id
		return order.user_id == user.id

	def get(self, request, pk):
		order = self.get_object(pk)
		if order is None:
			return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

		if not self.can_view_order(request.user, order):
			return Response({'message': 'You cannot view this order.'}, status=status.HTTP_403_FORBIDDEN)

		serializer = OrderSerializer(order)
		return Response(serializer.data)

	def put(self, request, pk):
		return self._update_order(request, pk, partial=False)

	def patch(self, request, pk):
		return self._update_order(request, pk, partial=True)

	def _update_order(self, request, pk, partial):
		order = self.get_object(pk)
		if order is None:
			return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

		if user_is_manager(request.user):
			data = {
				'delivery_crew': request.data.get('delivery_crew', order.delivery_crew_id),
				'status': request.data.get('status', order.status),
			}

			delivery_crew_id = data.get('delivery_crew')
			if delivery_crew_id is not None:
				try:
					crew_user = User.objects.get(id=delivery_crew_id)
				except User.DoesNotExist:
					return Response({'message': 'Delivery crew user not found.'}, status=status.HTTP_400_BAD_REQUEST)

				if not crew_user.groups.filter(name='Delivery crew').exists():
					return Response({'message': 'User is not in Delivery crew group.'}, status=status.HTTP_400_BAD_REQUEST)

			serializer = OrderSerializer(order, data=data, partial=partial)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		if user_is_delivery_crew(request.user):
			if order.delivery_crew_id != request.user.id:
				return Response({'message': 'You can only update assigned orders.'}, status=status.HTTP_403_FORBIDDEN)

			if 'status' not in request.data:
				return Response({'message': 'Only status can be updated.'}, status=status.HTTP_400_BAD_REQUEST)

			status_value = request.data.get('status')
			if status_value not in [0, 1, '0', '1']:
				return Response({'message': 'Status must be 0 or 1.'}, status=status.HTTP_400_BAD_REQUEST)

			order.status = int(status_value)
			order.save()
			serializer = OrderSerializer(order)
			return Response(serializer.data)

		return Response({'message': 'Not allowed to update this order.'}, status=status.HTTP_403_FORBIDDEN)

	def delete(self, request, pk):
		order = self.get_object(pk)
		if order is None:
			return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can delete orders.'}, status=status.HTTP_403_FORBIDDEN)

		order.delete()
		return Response({'message': 'Order deleted.'}, status=status.HTTP_200_OK)
