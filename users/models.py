from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    # 기존의 default Django User Model 중 일부 property를 무력화함
    # editable=False를 활용하여, '얘는 쓰지마'라고 하는 거임
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)

    # email 기준으로 계정관리하기 위헤 email을 unique
    email = models.EmailField(unique=True)

    # 기존 user data에 추가할 때 오류 방지 위해, default 넣어줌
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
