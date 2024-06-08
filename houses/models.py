from django.db import models
from django.conf import settings


class House(models.Model):
    """Model Definition for Houses"""

    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField(
        verbose_name="Price", help_text="Positive Numbers Only"
    )
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(
        verbose_name="Pets Allowed?",
        default=True,
        help_text="Does this house allow pets?",
    )

    # Forenier Keys
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    """Naming"""

    def __str__(self):
        return self.name
