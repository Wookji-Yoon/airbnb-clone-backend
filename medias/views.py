from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Photo
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT


class PhotoDetail(APIView):
    # 로그인 여부를 확인하는 shortcut
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            photo = Photo.objects.get(pk=pk)
            return photo
        except:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk=pk)
        if photo.room and photo.room.owner != request.user:
            raise PermissionDenied
        elif photo.experience and photo.experience.host != requst.user:
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_204_NO_CONTENT)
