from django.urls import path, include
from rest_framework import routers

from posts.views import PostModelViewSet

router = routers.SimpleRouter()
router.register(r'', PostModelViewSet)

urlpatterns = [
    path("", include(router.urls), name="게시글")
]
