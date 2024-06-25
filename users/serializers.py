from rest_framework.serializers import ModelSerializer
from .models import User


class UserTinySerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )
