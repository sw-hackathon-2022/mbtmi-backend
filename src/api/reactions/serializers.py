from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from posts.models import Post
from reactions.models import Like, Unlike


class PostLikeSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    count = SerializerMethodField()
    liked = SerializerMethodField()

    @extend_schema_field(serializers.IntegerField)
    def get_count(self, obj: Post):
        return obj.like_set.count()

    @extend_schema_field(serializers.BooleanField)
    def get_liked(self, obj: Post):
        return bool(Like.objects.filter(post_id=obj.id, user_id=self.context.get("request").user.id).first())


class PostUnlikeSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    count = SerializerMethodField()
    unliked = SerializerMethodField()

    @extend_schema_field(serializers.IntegerField)
    def get_count(self, obj: Post):
        return obj.unlike_set.count()

    @extend_schema_field(serializers.BooleanField)
    def get_unliked(self, obj: Post):
        return bool(Unlike.objects.filter(post_id=obj.id, user_id=self.context.get("request").user.id).first())


class PostReportSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PostReactionCountSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    like_count = SerializerMethodField()
    unlike_count = SerializerMethodField()

    @extend_schema_field(serializers.IntegerField)
    def get_like_count(self, obj: Post):
        return obj.like_set.count()

    @extend_schema_field(serializers.IntegerField)
    def get_unlike_count(self, obj: Post):
        return obj.unlike_set.count()
