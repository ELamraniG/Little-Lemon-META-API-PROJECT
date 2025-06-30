from django.urls import path

from users.views import (
    DeliveryCrewUsersView,
    DeliveryCrewUsersIdView,
    ManagerUsersView,
    ManagerUsersIdView,
)

urlpatterns = [
    path('groups/manager/users', ManagerUsersView.as_view()),
    path('groups/manager/users/<int:userId>', ManagerUsersIdView.as_view()),
    path('groups/delivery-crew/users', DeliveryCrewUsersView.as_view()),
    path('groups/delivery-crew/users/<int:userId>', DeliveryCrewUsersIdView.as_view()),
]
