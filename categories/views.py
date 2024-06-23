from django.shortcuts import render
from .models import Category
from django.http import JsonResponse


# Create your views here.
def categories(request):
    all_categories = Category.objects.all()
    return JsonResponse({"ok": True})
