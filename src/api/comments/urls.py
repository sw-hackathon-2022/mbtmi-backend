from django.urls import path
from comments.views import CommentCreateView, CommentDestroyView


urlpatterns = [
    path("", CommentCreateView.as_view(), name="덧글"),
    path("<int:comment_id>/", CommentDestroyView.as_view(), name="덧글")
]
