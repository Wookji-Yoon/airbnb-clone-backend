from rest_framework import serializers
from .models import Category

""" 5. serializer를 한번만 만들어두면 객체가 django모델에서 user쪽에서 원하는 것으로 번역해줄수 있다
6. serializer에게 user가 created_at과 pk는 보내지 않는다고 말하려면 read_only = True
7. serializer에게 어떤게 필요한지만 알려주면 된다 그럼 모델을 django에서 json으로 변역해줄거고 검증을 거쳐서 user데이터로 부터 모델을 만들수 있게해준다 """


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "name",
            "kind",
        )
        # fields = "__all__"로 모든 걸 보여주는 방법도 있음
        # 제외할 필드로 하고 싶으면 exclude
