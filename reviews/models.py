from django.db import models
from common.models import CommonModel
from django.conf import settings
from django.core.validators import MaxValueValidator

# Create your models here.


class Review(CommonModel):

    "Review for rooms or experiences"

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    rooms = models.ForeignKey(
        to="rooms.Room",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    experiences = models.ForeignKey(
        to="experiences.Experience",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user}_{self.rating}점"
