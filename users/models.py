from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        # 꼭 대문자일 필요는 없음
        # 첫번째는 value(데이터베이스), 두번째는 label임(admin 패널에서)
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        # 파이썬에서 .tuple 괄호는 생략 가능함
        WON = "won", "Korean Won"
        USD = "usd", "Dollar"

    # 기존의 default Django User Model 중 일부 property를 무력화함
    # editable=False를 활용하여, '얘는 쓰지마'라고 하는 거임
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)

    # email 기준으로 계정관리하기 위헤 email을 unique
    email = models.EmailField(unique=True)

    # 새로운 것들
    # 기존 user data에 추가할 때 오류 방지 위해, default 넣어줌
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices)
    currency = models.CharField(max_length=5, choices=CurrencyChoices.choices)

    # blank=true라고 하면 validate에서 필수가 아니게 한다. (데이터베이스에는 빈 문자열 ""이 저장된다.)
    # Null=True라고 하면 데이터베이스 필드에서 null값이 되게 된다.
    avatar = models.ImageField(blank=True)
