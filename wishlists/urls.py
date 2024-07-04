from django.urls import path
from .views import Wishlists, WishlistDetail, ToggleRoom

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>", WishlistDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", ToggleRoom.as_view()),
]
