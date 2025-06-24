from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/', include('menu.urls')),
    path('api/', include('users.urls')),
    path('api/', include('orders.urls')),
]
