from drf_spectacular.utils import extend_schema, extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    is_author = SerializerMethodField()
    user = serializers.CurrentUserDefault()

    class Meta:
        model = Comment
        exclude = ("post",)

    @extend_schema_field(serializers.BooleanField)
    def get_is_author(self, obj: Comment):
        return obj.author == self.context.get("login_user")
