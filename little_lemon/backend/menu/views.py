from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.models import MenuItem
from menu.serializers import MenuItemSerializer
from users.permissions import user_is_manager


class MenuItemsView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		items = MenuItem.objects.all()
		search_text = request.query_params.get('search')
		if search_text:
			items = items.filter(title__icontains=search_text)
		ordering = request.query_params.get('ordering', 'id')
		allowed = ['id', '-id', 'price', '-price', 'title', '-title']
		if ordering in allowed:
			items = items.order_by(ordering)

		paginator = PageNumberPagination()
		paginator.page_size_query_param = 'perpage'
		page = paginator.paginate_queryset(items, request)
		serializer = MenuItemSerializer(page, many=True)
		return paginator.get_paginated_response(serializer.data)

	def post(self, request):
		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can add menu items.'}, status=status.HTTP_403_FORBIDDEN)

		serializer = MenuItemSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleMenuItemView(APIView):
	permission_classes = [IsAuthenticated]

	def get_object(self, pk):
		try:
			return MenuItem.objects.get(pk=pk)
		except MenuItem.DoesNotExist:
			return None

	def get(self, request, pk):
		item = self.get_object(pk)
		if item is None:
			return Response({'message': 'Menu item not found.'}, status=status.HTTP_404_NOT_FOUND)
		serializer = MenuItemSerializer(item)
		return Response(serializer.data)

	def put(self, request, pk):
		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can update menu items.'}, status=status.HTTP_403_FORBIDDEN)

		item = self.get_object(pk)
		if item is None:
			return Response({'message': 'Menu item not found.'}, status=status.HTTP_404_NOT_FOUND)

		serializer = MenuItemSerializer(item, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk):
		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can update menu items.'}, status=status.HTTP_403_FORBIDDEN)

		item = self.get_object(pk)
		if item is None:
			return Response({'message': 'Menu item not found.'}, status=status.HTTP_404_NOT_FOUND)

		serializer = MenuItemSerializer(item, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can delete menu items.'}, status=status.HTTP_403_FORBIDDEN)

		item = self.get_object(pk)
		if item is None:
			return Response({'message': 'Menu item not found.'}, status=status.HTTP_404_NOT_FOUND)

		item.delete()
		return Response({'message': 'Menu item deleted.'}, status=status.HTTP_200_OK)
