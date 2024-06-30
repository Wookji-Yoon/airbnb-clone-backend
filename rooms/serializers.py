from rest_framework.serializers import SerializerMethodField, ModelSerializer
from .models import Amenity, Room

from users.serializers import UserTinySerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):

    class Meta:
        model = Amenity
        fields = "__all__"


class RoomDetailSerializer(ModelSerializer):

    # 관계형 데이터에 다른 시리얼라이저를 설정해서 depth=1에서 어떻게 보일지  설정할 수 있다.
    # read_only=True를 해서 User가 Post할 떄는 입력하지 않아도 되게 할 수 있다. 또는
    owner = UserTinySerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    # MethodField를 사용해서, model에 없는 field를 만들 수 있다.
    rating = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"
        # depth=1이라고 넣으면, 관계성 있는 data가 ID만 있는 게 아니라 확장된다.
        # 그러나 그만큼 Data가 많이 든다는 걸 조심해야 할 걸!
        # 그리고 커스터마이징도 불가능하지!
        depth = 1

    def get_rating(self, room):
        # 이 함수는 RoomDetailSerializer의 rating을 위한 함수이다.
        # 반드시 field 앞에 get_를 붙여야 한다.
        # 두번째 object로는 이 method를 호출한 object가 들어간다.

        return room.rating()


class RoomListSerializer(ModelSerializer):

    rating = SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
        )

    def get_rating(self, room):
        # 이 함수는 RoomDetailSerializer의 rating을 위한 함수이다.
        # 반드시 field 앞에 get_를 붙여야 한다.
        # 두번째 object로는 이 method를 호출한 object가 들어간다.

        return room.rating()
