from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from comments.serializers import CommentSerializer
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    comments = SerializerMethodField()
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

    def comments(self, obj: Post):
        return CommentSerializer(obj.comment_set, many=True,
                                 source="comment_set",
                                 context={
                                     "request": self.context.get("request")}
                                 ).data

    def get_like_count(self, obj: Post):
        return obj.like_set.count()

    def get_unlike_count(self, obj: Post):
        return obj.unlike_set.count()
