from django.db import models
from common.models import CommonModel

# Create your models here.


class Category(CommonModel):
    """Room or Expereience Category"""

    class CategoryKindChoices(models.TextChoices):
        ROOMS = ("rooms", "Rooms")
        EXPERIENCES = ("experiences", "Experiences")

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=20,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self):
        return f"{self.kind}_{self.name}"

    class Meta:
        verbose_name_plural = "카테고리들"
