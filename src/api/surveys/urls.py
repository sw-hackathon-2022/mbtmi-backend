from django.urls import path

from surveys.views import SurveyListView, SurveyReplyView


urlpatterns = [
    path("", SurveyListView.as_view(), name="설문 목록"),
    path("<int:survey_id>/items/<int:item_id>", SurveyReplyView.as_view(), name="설문 응답")
]
