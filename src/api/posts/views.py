from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets
from rest_framework.response import Response

from posts.filters import PostByMBTIFilterBackend
from posts.models import Post
from posts.serializers import PostSerializer, PostDetailSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["/posts"],
        operation_id="게시글 목록 조회",
        description="게시글 정보/반응 목록 조회",
        parameters=[
            OpenApiParameter(name="mbti", description="(필터) 작성자 MBTI(ex. mbti=E,S,I,F,J,T", type=str)
        ]
    ),
    create=extend_schema(
        tags=["/posts"],
        operation_id="게시글 등록",
        description="제목/본문 정보로 게시글 등록",
    ),
    update=extend_schema(
        tags=["/posts"],
        operation_id="게시글 수정",
        description="게시글 제목/본문 수정",
    ),
    destroy=extend_schema(
        tags=["/posts"],
        operation_id="게시글 삭제",
        description="게시글 삭제",
    ),
    retrieve=extend_schema(
        tags=["/posts"],
        operation_id="게시글 상세 조회",
        description="게시글 정보 / 반응 정보(반응수, 반응 여부) 조회",
    )
)
class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").all()
    serializer_class = PostSerializer
    http_method_names = [
        "get",
        "post",
        "put",
        "delete",
    ]
    lookup_field = "id"
    lookup_url_kwarg = "post_id"
    filter_backends = (PostByMBTIFilterBackend,)

    def get_detail_serializer(self, *args, **kwargs):
        serializer_class = PostDetailSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_detail_serializer(instance)
        return Response(serializer.data)
