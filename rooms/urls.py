from django.urls import path
from . import views

urlpatterns = [
    path("", views.see_all_room),
    # 파라미터를 넣는 방법은 아래와 같다.
    path("<int:room_id>", views.see_one_room),
]
