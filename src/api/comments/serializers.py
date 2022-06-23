from drf_spectacular.utils import extend_schema, extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from comments.models import Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):

    is_mine = SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ("post",)

    @extend_schema_field(serializers.BooleanField)
    def get_is_mine(self, obj: Comment):
        return obj.author == self.context.get("request").user
