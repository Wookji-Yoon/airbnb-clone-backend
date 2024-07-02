from rest_framework import serializers
from .models import Review
from users.serializers import UserTinySerializer


class ReviewSerializer(serializers.ModelSerializer):

    user = UserTinySerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("user", "payload", "rating")
