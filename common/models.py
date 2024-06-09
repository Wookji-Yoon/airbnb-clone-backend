from django.db import models


class CommonModel(models.Model):
    """Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta는 장고에서 model을 configure할 때 쓴다
    class Meta:
        # abstract이라고 설정하면, 장고가 얘를 데이터베이스에 넣지 않는다.
        abstract = True
