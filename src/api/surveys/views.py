from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from surveys import schemas
from surveys.models import Survey, SurveyReply
from surveys.serializers import SurveyReplySerializer, SurveySerializer


@extend_schema(
    tags=["/surveys"],
    operation_id="설문 목록 조회",
    description="설문 목록과 설문별 항목을 조회(replied_item: 응답 항목의 id(응답 완료한 설문), null(미응답 설문))",
    responses=inline_serializer(
        name="SurveyAPIResponseSerializer",
        fields={
            "surveys": SurveySerializer(many=True)
        },
        many=False
    ),
    examples=schemas.SURVEY_LIST_EXAMPLES
)
class SurveyListView(GenericAPIView):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"surveys": serializer.data})


@extend_schema(
    tags=["/surveys"],
    operation_id="설문 응답 등록",
    description="설문과 항목을 선택하여 응답 등록, 응답 결과 리턴",
    request=None,
)
class SurveyReplyView(CreateAPIView):
    serializer_class = SurveyReplySerializer
    queryset = SurveyReply.objects.all()

    def perform_create(self, serializer):
        try:
            survey_id = self.kwargs["survey_id"]
            item_id = self.kwargs["item_id"]
            conflict_object = SurveyReply.objects.filter(item_id=item_id, replier=self.request.user).first()
            if conflict_object:
                raise APIException(code=status.HTTP_409_CONFLICT, detail="already replied survey")
            serializer.save(item_id=item_id)
        except KeyError:
            raise APIException(code=status.HTTP_400_BAD_REQUEST, detail="invalid path parameters")
