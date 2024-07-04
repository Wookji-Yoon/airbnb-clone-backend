from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_200_OK,
)

from .serializers import WishlistSerializer, WishlistDetailSerializer
from .models import Wishlist
from rooms.models import Room


# Create your views here.
class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            new_wishlist = serializer.save(user=request.user)
            return Response(WishlistSerializer(new_wishlist).data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            get_wishlist = Wishlist.objects.get(pk=pk)
            return get_wishlist
        except:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk=pk)
        serializer = WishlistDetailSerializer(wishlist, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk=pk)
        if wishlist.user != request.user:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
        wishlist.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ToggleRoom(APIView):

    permission_classes = [IsAuthenticated]

    def get_wishlist(self, pk):
        try:
            return Wishlist.objects.get(pk=pk)
        except Wishlist.DoesNotExist:
            raise NotFound("Wishlist not found")

    def get_room(self, room_pk):
        try:
            return Room.objects.get(pk=room_pk)
        except Room.DoesNotExist:
            raise NotFound("Room not found")

    def put(self, request, pk, room_pk):
        wishlist = self.get_wishlist(pk=pk)
        room = self.get_room(room_pk=room_pk)

        if wishlist.user != request.user:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)

        if wishlist.rooms.filter(pk=room_pk).exists:
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)

        return Response(status=HTTP_200_OK)
