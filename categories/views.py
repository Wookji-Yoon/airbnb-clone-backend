from django.shortcuts import render
from .models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer


# api_view를 데코레이터로 붙이고, Reponse를 레스트프레임워크 리스폰스로 하면 된다.
@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        # Serializer는 Quesyset을 JSON으로 바꾸어준다.
        serializer = CategorySerializer(all_categories, many=True)
        return Response({"ok": True, "cateogries": serializer.data})
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"created": True})
        else:
            return Response(serializer.errors)


@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response({"category": serializer.data})
