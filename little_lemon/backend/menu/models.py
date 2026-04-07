from django.db import models


class MenuItem(models.Model):
	title = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	inventory = models.IntegerField(default=0)

	def __str__(self):
		return self.title
