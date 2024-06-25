from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Amenity
from .serializers import AmenitySerializer


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
