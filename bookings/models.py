from django.db import models
from common.models import CommonModel
from django.conf import settings


# Create your models here.
class Booking(CommonModel):
    """wishlist that users can create"""

    class KindChoices(models.TextChoices):
        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"

    kind = models.CharField(max_length=30, choices=KindChoices.choices)

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    room = models.ForeignKey(
        to="rooms.Room",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )
    experience = models.ForeignKey(
        to="experiences.Experience",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )

    room_check_in_date = models.DateField(null=True, blank=True)
    room_check_out_date = models.DateField(null=True, blank=True)
    experience_time = models.DateTimeField(null=True, blank=True)

    guests = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user}의 예약"
