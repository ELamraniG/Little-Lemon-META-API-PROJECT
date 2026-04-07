from django.urls import path

from users.views import (
    DeliveryCrewGroupUsersView,
    DeliveryCrewSingleUserView,
    ManagerGroupUsersView,
    ManagerSingleUserView,
)

urlpatterns = [
    path('groups/manager/users', ManagerGroupUsersView.as_view()),
    path('groups/manager/users/<int:userId>', ManagerSingleUserView.as_view()),
    path('groups/delivery-crew/users', DeliveryCrewGroupUsersView.as_view()),
    path('groups/delivery-crew/users/<int:userId>', DeliveryCrewSingleUserView.as_view()),
]
