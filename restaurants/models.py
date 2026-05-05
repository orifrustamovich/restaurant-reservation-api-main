from django.db import models

from users.models import CustomUser


# Create your models here.
class Restaurant(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                              related_name="restaurants")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to="restaurants/", null=True, blank=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name="tables")
    table_number = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ["restaurant", "table_number"]
