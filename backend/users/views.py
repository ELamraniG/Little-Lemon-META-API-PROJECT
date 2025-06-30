from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import ensureDefaultGroups, isManager
from users.serializers import GroupUserSerializer


class ManagerUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not isManager(request.user):
            return Response({'message': 'Only managers can view group users.'}, status=status.HTTP_403_FORBIDDEN)

        managerGroup = Group.objects.get(name='Manager')
        users = managerGroup.user_set.all()
        serializer = GroupUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not isManager(request.user):
            return Response({'message': 'Only managers can add group users.'}, status=status.HTTP_403_FORBIDDEN)

        userId = request.data.get('userId')
        if not userId:
            return Response({'message': 'userId is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        managerGroup = Group.objects.get(name='Manager')
        managerGroup.user_set.add(user)
        return Response({'message': 'User added to Manager group.'}, status=status.HTTP_201_CREATED)


class ManagerUsersIdView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, userId):
        if not isManager(request.user):
            return Response({'message': 'Only managers can remove group users.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        managerGroup = Group.objects.get(name='Manager')
        managerGroup.user_set.remove(user)
        return Response({'message': 'User removed from Manager group.'}, status=status.HTTP_200_OK)


class DeliveryCrewUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not isManager(request.user):
            return Response({'message': 'Only managers can view group users.'}, status=status.HTTP_403_FORBIDDEN)

        deliveryGroup = Group.objects.get(name='Delivery crew')
        users = deliveryGroup.user_set.all()
        serializer = GroupUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not isManager(request.user):
            return Response({'message': 'Only managers can add group users.'}, status=status.HTTP_403_FORBIDDEN)

        userId = request.data.get('userId')
        if not userId:
            return Response({'message': 'userId is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        deliveryGroup = Group.objects.get(name='Delivery crew')
        deliveryGroup.user_set.add(user)
        return Response({'message': 'User added to Delivery crew group.'}, status=status.HTTP_201_CREATED)


class DeliveryCrewUsersIdView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, userId):
        if not isManager(request.user):
            return Response({'message': 'Only managers can remove group users.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        deliveryGroup = Group.objects.get(name='Delivery crew')
        deliveryGroup.user_set.remove(user)
        return Response({'message': 'User removed from Delivery crew group.'}, status=status.HTTP_200_OK)
