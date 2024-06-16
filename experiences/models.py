from django.db import models
from common.models import CommonModel
from django.conf import settings

# Create your models here.


class Experience(CommonModel):
    """Expereience Model Definition"""

    name = models.CharField(max_length=150, default="")
    country = models.CharField(max_length=50, default="대한민국")
    city = models.CharField(max_length=80, default="서울")

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="experiences",
    )

    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()

    perks = models.ManyToManyField(
        to="experiences.Perk",
        related_name="experiences",
    )

    category = models.ForeignKey(
        to="categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    """What is included in experiences"""

    name = models.CharField(max_length=150, default="")

    # 필드가 캐릭터필드나 텍스트필드일 경우 반드시 null=True를 할 필요는 없다.
    # 빈칸도 괜찮기 때문, 다만 defualt=""는 하자
    details = models.CharField(max_length=250, blank=True, default="")
    explanation = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name
