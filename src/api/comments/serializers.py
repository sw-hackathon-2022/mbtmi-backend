from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from comments.models import Comment
from posts.models import Post
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):

    is_mine = SerializerMethodField()
    author = UserSerializer()

    class Meta:
        model = Comment
        exclude = ("post",)
        read_only_fields = ("__all__",)

    @extend_schema_field(serializers.BooleanField)
    def get_is_mine(self, obj: Comment):
        return obj.author == self.context.get("request").user


class CommentCrationSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ("author", "content",)
