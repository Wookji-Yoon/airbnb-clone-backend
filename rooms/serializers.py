from rest_framework.serializers import SerializerMethodField, ModelSerializer
from .models import Amenity, Room
from wishlists.models import Wishlist
from users.serializers import UserTinySerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer


class AmenitySerializer(ModelSerializer):

    class Meta:
        model = Amenity
        fields = "__all__"


class RoomDetailSerializer(ModelSerializer):

    # 관계형 데이터에 다른 시리얼라이저를 설정해서 depth=1에서 어떻게 보일지  설정할 수 있다.
    # read_only=True를 해서 User가 Post할 떄는 입력하지 않아도 되게 할 수 있다.
    owner = UserTinySerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    # MethodField를 사용해서, model에 없는 field를 만들 수 있다.
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()

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

        # context를 활용하면 serializer를 사용하는 view에서 context에 데이터를 담아 보내서 동적 field를 만들 수 있다.

    def get_is_owner(self, room):
        request = self.context["request"]
        if room.owner == request.user:
            return True
        else:
            return False


class RoomListSerializer(ModelSerializer):

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "is_liked",
            "reviews",
            "photos",
        )

    def get_rating(self, room):
        # 이 함수는 RoomDetailSerializer의 rating을 위한 함수이다.
        # 반드시 field 앞에 get_를 붙여야 한다.
        # 두번째 object로는 이 method를 호출한 object가 들어간다.

        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        if room.owner == request.user:
            return True
        else:
            return False

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user,
            rooms__pk=room.pk,
        ).exists()
