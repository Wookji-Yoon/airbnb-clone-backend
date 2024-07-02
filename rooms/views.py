from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomDetailSerializer, RoomListSerializer
from django.db import transaction
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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

    # get일때는 괜찮고, put, post, delete일 때만 authenticated를 확인한다.
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_items = Room.objects.all()
        serializer = RoomListSerializer(
            all_items,
            many=True,
            context={"request": request},
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
                    owner=owner,
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
        serializer = RoomDetailSerializer(
            get_item,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        get_item = self.get_object(pk)

        # 로그인하지 않았으면 작동 안함
        if not request.user.is_authenticated:
            raise NotAuthenticated

        # 자기가 방주인이 아니면 작동안함
        if get_item.owner != request.user:
            raise PermissionDenied

        get_item.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        get_item = self.get_object(pk)

        # 로그인하지 않았으면 작동 안함
        if not request.user.is_authenticated:
            raise NotAuthenticated

        # 자기가 방주인이 아니면 작동안함
        if get_item.owner != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(
            instance=get_item,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if serializer.is_valid():

            # save_kwargs를 만들어 변동이 있을 때만 저장하도록 한다.
            save_kwargs = {}

            if "category" in request.data:
                category_pk = request.data.get("category")
                if category_pk is None:
                    raise ParseError("Category pk is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind != Category.CategoryKindChoices.ROOMS:
                        raise ParseError("Category should be 'Rooms'")
                    save_kwargs["category"] = category
                except Category.DoesNotExist:
                    raise ParseError("Cannot find Category")

            if "amenities" in request.data:
                pk_list = request.data.get("amenities")
                amenities = []
                for amenity_pk in pk_list:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        amenities.append(amenity)
                    except Amenity.DoesNotExist:
                        raise ParseError("Cannot find Amenity")
                save_kwargs["amenities"] = amenities

            new_item = serializer.save(**save_kwargs)

            return Response(RoomDetailSerializer(new_item).data)
        else:
            return Response(serializer.errors)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):

        # query는 따로 설정안해도 컨트롤할 수 있다.
        page = request.query_params.get("page", default=1)
        try:
            page = int(page)
        except ValueError:
            page = 1

        pagination_size = 5
        start = (page - 1) * pagination_size
        end = page * pagination_size

        get_item = self.get_object(pk=pk)

        # django가 자르는 게 아니라 database에 요청할 때부터 잘라서 가기 때문에 최적화가 굉장히 좋아진다
        reviews = get_item.reviews.all()[start:end]

        serializer = ReviewSerializer(
            reviews,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            room = self.get_object(pk=pk)
            new_review = serializer.save(
                user=user,
                rooms=room,
            )
            return Response(ReviewSerializer(new_review).data)
        else:
            return Response(serializer.errors)


class RoomAmenities(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):

        # query는 따로 설정안해도 컨트롤할 수 있다.
        page = request.query_params.get("page", default=1)
        try:
            page = int(page)
        except ValueError:
            page = 1

        pagination_size = 5
        start = (page - 1) * pagination_size
        end = page * pagination_size

        get_item = self.get_object(pk=pk)

        # django가 자르는 게 아니라 database에 요청할 때부터 잘라서 가기 때문에 최적화가 굉장히 좋아진다
        amenities = get_item.amenities.all()[start:end]

        serializer = AmenitySerializer(
            amenities,
            many=True,
        )

        return Response(serializer.data)


class RoomPhotos(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def post(self, request, pk):
        get_item = self.get_object(pk)

        # 로그인하지 않았으면 작동 안함
        if not request.user.is_authenticated:
            raise NotAuthenticated

        # 자기가 방주인이 아니면 작동안함
        if get_item.owner != request.user:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)

        if serializer.is_valid():
            photo = serializer.save(room=get_item)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(serializer.errors)
