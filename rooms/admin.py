from django.contrib import admin
from .models import Room, Amenity

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "kind", "owner")
    list_filter = ("name", "price", "rooms")
    list_display_links = ("name", "kind")


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")

    readonly_fields = ("created_at", "updated_at")
