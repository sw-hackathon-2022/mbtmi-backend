from rest_framework import serializers

from users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["mbti", "about"]
        extra_kwargs = {
            "mbti": {
                "required": True,
            }
        }
