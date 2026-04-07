from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from menu.models import MenuItem


class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	unit_price = models.DecimalField(max_digits=6, decimal_places=2)
	price = models.DecimalField(max_digits=8, decimal_places=2)


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
	delivery_crew = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='delivery_orders',
	)
	status = models.IntegerField(default=0)
	total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	date = models.DateField(default=timezone.now)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
	menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	unit_price = models.DecimalField(max_digits=6, decimal_places=2)
	price = models.DecimalField(max_digits=8, decimal_places=2)
