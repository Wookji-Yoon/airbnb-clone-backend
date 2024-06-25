from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room

from users.serializers import UserTinySerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):

    class Meta:
        model = Amenity
        fields = "__all__"


class RoomDetailSerializer(ModelSerializer):

    # 관계형 데이터에 다른 시리얼라이저를 설정해서 depth=1에서 어떻게 보일지  설정할 수 있다.
    owner = UserTinySerializer()
    amenities = AmenitySerializer(many=True)
    categories = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"
        # depth=1이라고 넣으면, 관계성 있는 data가 ID만 있는 게 아니라 확장된다.
        # 그러나 그만큼 Data가 많이 든다는 걸 조심해야 할 걸!
        # 그리고 커스터마이징도 불가능하지!
        depth = 1


class RoomListSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
