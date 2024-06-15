from django.db import models
from common.models import CommonModel
from django.conf import settings


# Create your models here.
class Wishlist(CommonModel):
    """wishlist that users can create"""

    name = models.CharField(max_length=30)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    rooms = models.ManyToManyField(to="rooms.Room", blank=True)

    experiences = models.ManyToManyField(to="experiences.Experience", blank=True)

    def __str__(self):
        return self.name
