from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, DestroyAPIView, get_object_or_404

from comments.models import Comment
from comments.serializers import CommentSerializer, CommentCrationSerializer
from posts.models import Post


@extend_schema(
    tags=["/comments"],
    operation_id="덧글 등록",
    description="덧글 등록",
)
class CommentCreateView(CreateAPIView):
    serializer_class = CommentCrationSerializer
    queryset = Comment.objects.select_related("post").all()
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"

    def perform_create(self, serializer):
        post_queryset = Post.objects.all()
        post = get_object_or_404(post_queryset, id=self.kwargs["post_id"])
        serializer.save(post=post)


@extend_schema(
    tags=["/comments"],
    operation_id="덧글 삭제",
    description="덧글 삭제",
)
class CommentDestroyView(DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.select_related("post").all()
    lookup_field = "id"
    lookup_url_kwarg = "comment_id"
