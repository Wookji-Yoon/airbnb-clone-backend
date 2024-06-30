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
                # nested field에 해당하는 애들을 serializer로 valid할 수는 있다. 그런데, 이것을 곧바로 save한다고 알맞게 data를 생성하지 못한다.
                # 따라서 두 가지 조치가 필요하다.
                # 1. save단계에서 유저가 보낸 data가 곧바로 넘어가지 못하도록 serializer에 read_only = True를 걸어야 한다.
                # 2. save의 parameter로 관계를  explicit해야 한다.
                category_pk = request.data.get("category")
                if category_pk is None:
                    raise ParseError("Category pk is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind != Category.CategoryKindChoices.ROOMS:
                        raise ParseError("Cateogry shoud be 'rooms'")
                except category.DoesNotExist:
                    raise ParseError("Cannot find Cateogry")

                with transaction.atomic():

                    new_item = serializer.save(
                        owner=request.user,
                        category=category,
                    )

                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        new_item.amenities.add(amenity)

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
