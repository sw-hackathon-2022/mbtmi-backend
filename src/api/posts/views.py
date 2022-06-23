from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from posts.models import Post
from posts.serializers import PostSerializer


@extend_schema_view(
    operation_id="게시글",
    tags=["/posts"],
    list=extend_schema(
        operation_id="게시글 목록 조회",
        description="게시글 정보/반응 목록 조회",
    ),
    create=extend_schema(
        operation_id="게시글 등록",
        description="제목/본문 정보로 게시글 등록",
    ),
    put=extend_schema(
        operation_id="게시글 수정",
        description="게시글 제목/본문 수정",
    ),
)
class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    http_method_names = [
        "get",
        "post",
        "put",
        "delete"
    ]

