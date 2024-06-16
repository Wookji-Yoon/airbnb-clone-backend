from django.contrib import admin
from .models import Room, Amenity

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "total_amenities_model",
        "total_amenities_admin",
        "owner",
    )
    list_filter = ("name",)
    list_display_links = ("name",)

    # ORM을 나중에 ADMin 모델에만 쓰고 있으면, admin의 method로 정의한다
    def total_amenities_admin(self, room):
        return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")

    readonly_fields = ("created_at", "updated_at")
