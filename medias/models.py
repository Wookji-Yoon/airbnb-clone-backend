from django.db import models
from common.models import CommonModel


# Create your models here.
class Photo(CommonModel):
    """Photo"""

    file = models.ImageField()
    description = models.CharField(max_length=150)

    room = models.ForeignKey(
        to="rooms.Room",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    experience = models.ForeignKey(
        to="experiences.Experience",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):
    """Video"""

    file = models.FileField()

    experience = models.OneToOneField(
        to="experiences.Experience",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Video File"
