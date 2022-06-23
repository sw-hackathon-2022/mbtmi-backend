from django.urls import path, include
from rest_framework import routers

from posts.views import PostModelViewSet, PostDetailView

router = routers.SimpleRouter()
router.register(r'', PostModelViewSet)

urlpatterns = [
    path("", include(router.urls), name="게시글"),
    path("<int:post_id>/", PostDetailView.as_view(), name="게시글 상세 조회")
]
