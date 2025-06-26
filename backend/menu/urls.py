from django.urls import path

from menu.views import MenuItemsView, MenuItemsIdView

urlpatterns = [
    path('menu-items', MenuItemsView.as_view()),
    path('menu-items/<int:pk>', MenuItemsIdView.as_view()),
]
