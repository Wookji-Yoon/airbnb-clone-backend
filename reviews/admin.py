from django.contrib import admin
from .models import Review


class RatingFilter(admin.SimpleListFilter):
    title = "Filter by Rating"

    # url에 어떻게 보일 것인지
    parameter_name = "starscore"

    # 3개의 parameter를 필수로 받는다.
    def lookups(self, request, model_admin):
        # 앞쪽은 데이터베이스, 뒤쪽은 admin에 나타나는 값
        return [("okay", "Okay"), ("good", "Good"), ("too much", "Too Much")]

    def queryset(self, request, reviews):
        # self.value를 하면 lookup 함수에서 선택된 값을 받는다.

        query = self.value()

        if query == "okay":
            return reviews.filter(rating__lte=10)
        elif query == "good":
            return reviews.filter(rating__lte=10000).filter(rating__gt=10)
        elif query == "too much":
            return reviews.filter(rating__gt=10000)

        return reviews


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("__str__", "rating", "payload", "rooms")
    list_filter = (RatingFilter,)
