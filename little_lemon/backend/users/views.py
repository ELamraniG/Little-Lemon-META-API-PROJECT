from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import ensure_default_groups, user_is_manager
from users.serializers import GroupUserSerializer


class ManagerGroupUsersView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can view group users.'}, status=status.HTTP_403_FORBIDDEN)

		ensure_default_groups()
		manager_group = Group.objects.get(name='Manager')
		users = manager_group.user_set.all()
		serializer = GroupUserSerializer(users, many=True)
		return Response(serializer.data)

	def post(self, request):
		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can add group users.'}, status=status.HTTP_403_FORBIDDEN)

		ensure_default_groups()
		user_id = request.data.get('userId')
		if not user_id:
			return Response({'message': 'userId is required.'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			user = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

		manager_group = Group.objects.get(name='Manager')
		manager_group.user_set.add(user)
		return Response({'message': 'User added to Manager group.'}, status=status.HTTP_201_CREATED)


class ManagerSingleUserView(APIView):
	permission_classes = [IsAuthenticated]

	def delete(self, request, userId):
		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can remove group users.'}, status=status.HTTP_403_FORBIDDEN)

		ensure_default_groups()
		try:
			user = User.objects.get(id=userId)
		except User.DoesNotExist:
			return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

		manager_group = Group.objects.get(name='Manager')
		manager_group.user_set.remove(user)
		return Response({'message': 'User removed from Manager group.'}, status=status.HTTP_200_OK)


class DeliveryCrewGroupUsersView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can view group users.'}, status=status.HTTP_403_FORBIDDEN)

		ensure_default_groups()
		delivery_group = Group.objects.get(name='Delivery crew')
		users = delivery_group.user_set.all()
		serializer = GroupUserSerializer(users, many=True)
		return Response(serializer.data)

	def post(self, request):
		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can add group users.'}, status=status.HTTP_403_FORBIDDEN)

		ensure_default_groups()
		user_id = request.data.get('userId')
		if not user_id:
			return Response({'message': 'userId is required.'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			user = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

		delivery_group = Group.objects.get(name='Delivery crew')
		delivery_group.user_set.add(user)
		return Response({'message': 'User added to Delivery crew group.'}, status=status.HTTP_201_CREATED)


class DeliveryCrewSingleUserView(APIView):
	permission_classes = [IsAuthenticated]

	def delete(self, request, userId):
		if not user_is_manager(request.user):
			return Response({'message': 'Only managers can remove group users.'}, status=status.HTTP_403_FORBIDDEN)

		ensure_default_groups()
		try:
			user = User.objects.get(id=userId)
		except User.DoesNotExist:
			return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

		delivery_group = Group.objects.get(name='Delivery crew')
		delivery_group.user_set.remove(user)
		return Response({'message': 'User removed from Delivery crew group.'}, status=status.HTTP_200_OK)
