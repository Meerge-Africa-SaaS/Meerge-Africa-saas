from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "last_updated",
            "created",
            "email",
            "id",
            "username",
        ]
