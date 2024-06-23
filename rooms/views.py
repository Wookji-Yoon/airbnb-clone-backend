from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# Create your views here.
def see_all_room(request):
    # objects는 모델과 소통할 수 있게 하는 API 매니저
    rooms = Room.objects.all()

    # render의 context argument는 html에 변수를 넘기는 것
    # 보낸 변수는 html에서 {{}} 안에 넣어서 쓴다.
    return render(
        request,
        "all_rooms.html",
        context={
            "rooms": rooms,
            "title": "Hello, This is my first html",
        },
    )


def see_one_room(request, room_id):
    return HttpResponse(room_id)
