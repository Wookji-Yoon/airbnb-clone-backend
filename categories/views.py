from django.shortcuts import render
from .models import Category
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .serializers import CategorySerializer


class Categories(APIView):

    def get(self, request):
        all_categories = Category.objects.all()
        # Serializer는 Quesyset을 JSON으로 바꾸어준다.
        serializer = CategorySerializer(all_categories, many=True)
        return Response({"ok": True, "cateogries": serializer.data})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"created": True})
        else:
            return Response(serializer.errors)


class CategoryDetail(APIView):

    # URL의 상세한 부분을 작업할 때는 get_object로 객체를 가져온 뒤 get, put 등에 할당하는 것이 컨벤션이다.
    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
        return category

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk=pk))
        return Response({"category": serializer.data})

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk=pk),
            data=request.data,
            # partial라고 하면 property를 몇개만 보내도 적합하게 validatio해준다.
            partial=True,
        )
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk=pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
