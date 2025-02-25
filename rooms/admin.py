from django.contrib import admin
from .models import Room, Amenity

# Register your models here.


# 필수로 3가지 parameter를 넣어야 한다. 어떤 어드민인지, 어떤 유저가 요청하는지, 내가 선택한 요소들
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    list_display = (
        "name",
        "total_amenities_model",
        "total_amenities_admin",
        "owner",
        "rating",
        "price",
    )
    list_filter = ("name", "owner__is_host")
    list_display_links = ("name",)

    # search fields에서 장고는 기본적으로 __contain을 연산자를 활용한다.
    # ^를 앞에 붙이면 __startswith를 쓴다.
    # =를 앞에 붙이면 __exact를 쓴다
    # foreignkey로 검색하기 위해 owner__username이런 식으로 할 수 있다.
    search_fields = ("^name", "=price", "owner__username")

    # ORM을 나중에 ADMin 모델에만 쓰고 있으면, admin의 method로 정의한다
    def total_amenities_admin(self, room):
        return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")

    readonly_fields = ("created_at", "updated_at")
