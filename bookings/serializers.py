from .models import Booking
from rest_framework import serializers
from django.utils import timezone


class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "room_check_in_date",
            "room_check_out_date",
            "guests",
        )


# Data를 보여주기 위한 Serailizer랑 Data를 만드릭 위한 Serializer를 따로 쓰는 게 일반적
class CreateBookingSerializer(serializers.ModelSerializer):

    # 몇몇 field를 업데이트해서 required로 만든다. (model에서는 required가 아니기때문에) 따라서, serializer가 validation할 수 잇게 한다.
    room_check_in_date = serializers.DateField()
    room_check_out_date = serializers.DateField()

    # 그렇지만 좀 더 customize한 validation이 필요하다면 어떨까?
    # validate_{field} 형태의 method를 만들면 된다.
    def validate_room_check_in_date(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Late Booking Error")
        return value

    def validate_room_check_out_date(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Late Booking Error")
        return value

    # 그냥 validate함수를 만들면 모든 field를 한번에 validation한다.
    def validate(self, data):
        if data["room_check_out_date"] <= data["room_check_in_date"]:
            raise serializers.ValidationError(
                "Check in should bee smaller than check out"
            )

        if Booking.objects.filter(
            room_check_out__gt=data["room_check_in_date"],
            room_check_in_date__lt=data["room_check_out_date"],
            room=self.context["room"],
        ):
            raise serializers.ValidationError("Already Booking")

        return data

    class Meta:
        model = Booking
        fields = (
            "room_check_in_date",
            "room_check_out_date",
            "guests",
        )
