from django.db import models
from common.models import CommonModel
from django.conf import settings

# Create your models here.


class ChattingRoom(CommonModel):

    user = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name="chattingrooms",
    )

    def __str__(self):
        return "Chatting Room"


class Message(CommonModel):

    payload = models.TextField()
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="dms",
    )

    chattingroom = models.ForeignKey(
        to="dms.ChattingRoom",
        on_delete=models.CASCADE,
        related_name="dms",
    )

    def __str__(self):
        return f"{self.user} says: {self.payload}"
