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


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="get_shortten_username")

    class Meta:
        model = User
        fields = ("username", "mbti")
        read_only_fields = ("username", "mbti")


class UserDetailSerializer(serializers.ModelSerializer):
    username_shortten = serializers.CharField(source="get_shortten_username")

    class Meta:
        model = User
        fields = (
            "id",
            "mbti",
            "email",
            "username",
            "username_shortten",
            "about",
        )
        read_only_fields = (
            "id",
            "mbti",
            "email",
            "username",
            "username_shortten",
            "about",
        )
