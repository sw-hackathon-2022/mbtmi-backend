from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField

from comments.serializers import CommentSerializer
from posts.models import Post
from reactions.serializers import PostLikeSerializer, PostUnlikeSerializer, PostReactionCountSerializer
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    reactions = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "reactions",
        ]
        read_only_fields = (
            "id",
            "author",
            "created_at",
            "reactions",
        )

    @extend_schema_field(PostReactionCountSerializer)
    def get_reactions(self, obj: Post):
        return PostReactionCountSerializer(obj).data


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
