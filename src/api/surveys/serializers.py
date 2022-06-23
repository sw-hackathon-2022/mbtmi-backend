from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from surveys.models import Survey, SurveyItem, SurveyReply


class SurveyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyItem
        fields = (
            "id",
            "content",
        )
        read_only_fields = (
            "id",
            "content"
        )


class SurveySerializer(serializers.ModelSerializer):

    replied_item = SerializerMethodField()
    items = SerializerMethodField()

    class Meta:
        model = Survey
        fields = (
            "id",
            # "author",
            "content",
            "created_at",
            "deadline",
            "replied_item",
            "items",
        )

        read_only_fields = (
            "id",
            # "author",
            "content",
            "created_at",
            "deadline",
            "replied_item",
            "items",
        )

    @extend_schema_field(SurveyItemSerializer(many=True))
    def get_items(self, obj: Survey):
        return SurveyItemSerializer(obj.surveyitem_set, many=True).data

    @extend_schema_field(serializers.IntegerField)
    def get_replied_item(self, obj: Survey):
        _login_user = self.context.get("request").user
        replied_item = SurveyItem.objects.filter(survey=obj, surveyreply__replier=_login_user).first()
        return replied_item.id if replied_item else None



class SurveyReplySerializer(serializers.ModelSerializer):

    replier = serializers.HiddenField(default=serializers.CurrentUserDefault())
    result_items = SerializerMethodField()

    class Meta:
        model = SurveyReply
        fields = (
            "id",
            "replier",
            "created_at",
            "result_items",
        )
        read_only_fields = (
            "id",
            "replier",
            "created_at",
            "result_items",
        )

    @extend_schema_field(SurveyItemSerializer(many=True))
    def get_result_items(self, obj: SurveyReply):
        return SurveyItemSerializer(obj.item.survey.surveyitem_set, many=True).data
