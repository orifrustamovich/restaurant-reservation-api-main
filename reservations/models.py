from django.db import models

from users.models import CustomUser
from restaurants.models import Table

class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 related_name="reservations")
    table = models.ForeignKey(Table, on_delete=models.CASCADE,
                              related_name="reservations")
    reservation_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    party_size = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices,
                              default=Status.PENDING)
    special_requests = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_past(self):
        from django.utils import timezone
        reservation_dt = timezone.datetime.combine(
            self.reservation_date, self.start_time,
            tzinfo=timezone.get_current_timezone())
        return reservation_dt < timezone.now()

    def can_be_cancelled(self):
        return (not self.is_past() and
                self.status in [self.Status.PENDING, self.Status.CONFIRMED])

