from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):

    is_author = SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ("post",)

    def get_is_author(self, obj: Comment):
        return obj.author == serializers.CurrentUserDefault()
