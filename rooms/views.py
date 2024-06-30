from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomDetailSerializer, RoomListSerializer
from django.db import transaction


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializers = AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializers.data)

    def post(self, request):
        serializers = AmenitySerializer(data=request.data)
        if serializers.is_valid():
            amenity = serializers.save()
            # 새롭게 만들어진 amenity도 당연히 seralize해야한다!
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializers.errors)


class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            instance=amenity,
            data=request.data,
            # 만약 partial이 False라고 하더라도 다른 필드들이 required가 아니면 유효성검사에 통과할 수 있다.
            partial=True,
        )
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(AmenitySerializer(new_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):

    def get(self, request):
        all_items = Room.objects.all()
        serializer = RoomListSerializer(
            all_items,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                # 아래부터의 각주와 코드는 #11.9 강의와 상관없이 내가 Refactoring한 것이다.

                # request.data에서 nested field의 pk를 받았을 때, serializer.is_valid()로 유효성 검사는 가능합니다. 하지만,
                # serializer.save()를 바로 사용하면 올바른 데이터 생성이 어렵습니다. 왜냐하면, 실제 저장해야 할 데이터는 pk가 아닌 모델의 인스턴스이기 때문입니다.
                # 따라서, pk로 해당 모델의 인스턴스를 찾아 serializer.save()에 인자로 전달해야 합니다.

                # A. owner: User 모델과 ForeignKey로 연결됩니다. request에서 찾습니다.
                owner = request.user

                # B. category: Category 모델과 ForeignKey로 연결됩니다. 'Rooms' 종류의 카테고리만 유효합니다.
                category_pk = request.data.get("category")
                if category_pk is None:
                    raise ParseError("Category pk is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind != Category.CategoryKindChoices.ROOMS:
                        raise ParseError("Category should be 'Rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Cannot find Category")

                # C. amenities: Amenity 모델과 ManyToManyField로 연결됩니다. 유효한 Amenity의 pk 리스트를 받습니다.
                pk_list = request.data.get("amenities")
                amenities = []
                for amenity_pk in pk_list:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        amenities.append(amenity)
                    except Amenity.DoesNotExist:
                        raise ParseError("Cannot find Amenity")

                # Nested Field에 해당하는 모델 인스턴스를 모두 가져왔으니, 이제 serializer.save()에 인자로 전달합니다.
                # 사용자 입력이 있더라도, owner, category, amenities는 여기서 명시적으로 지정된 값으로 덮어쓰기 됩니다.
                # 이는 악의적/잘못된 사용자 데이터가 최종 데이터에 영향을 미치지 않도록 보장합니다.
                # 그러나 API 문서의 명확성을 위해, 이 필드들을 serializer에서 read_only=True로 설정하는 것이 좋습니다.
                new_item = serializer.save(
                    owner=request.user,
                    category=category,
                    amenities=amenities,
                )

                return Response(RoomDetailSerializer(new_item).data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        get_item = self.get_object(pk)
        serializer = RoomDetailSerializer(get_item)
        return Response(serializer.data)
