from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_field, extend_schema_serializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CurrentUserDefault
from rest_framework.serializers import ListSerializer

from comments.serializers import CommentSerializer
from posts.models import Post
from reactions.serializers import PostLikeSerializer, PostUnlikeSerializer
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comments = CommentSerializer(many=True, source="comment_set",
                                 context={"login_user": CurrentUserDefault()})
    like_count = SerializerMethodField()
    unlike_count = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "comments",
            "like_count",
            "unlike_count"
        ]
        read_only_fields = (
            "id",
            "author",
            "created_at",
            "comments",
            "like_count",
            "unlike_count"
        )

    @extend_schema_field(ListSerializer(child=CommentSerializer()))
    def get_comments(self, obj: Post):
        return CommentSerializer(obj.comment_set, many=True,
                                 source="comment_set",
                                 context={
                                     "request": self.context.get("request")}
                                 ).data

    @extend_schema_field(serializers.IntegerField)
    def get_like_count(self, obj: Post):
        return obj.like_set.count()

    @extend_schema_field(serializers.IntegerField)
    def get_unlike_count(self, obj: Post):
        return obj.unlike_set.count()


class PostDetailSerializer(serializers.ModelSerializer):
    comments = SerializerMethodField()
    like = SerializerMethodField()
    unlike = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "comments",
            "like",
            "unlike"
        ]
        read_only_fields = (
            "id",
            "author",
            "created_at",
            "comments",
            "like",
            "unlike"
        )

    @extend_schema_field(CommentSerializer(many=True))
    def get_comments(self, obj: Post):
        return CommentSerializer(obj.comment_set,
                                 many=True,
                                 source="comment_set",
                                 context={
                                     "request": self.context.get("request")
                                 }).data

    def get_like(self, obj: Post):
        return PostLikeSerializer(obj, context={"request": self.context.get("request")}).data

    def get_unlike(self, obj: Post):
        return PostUnlikeSerializer(obj, context={"request": self.context.get("request")}).data
