from django.db.models import Q
from rest_framework import filters
from rest_framework.request import Request

from posts.models import Post


class PostByMBTIFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset, view):
        if request.method == "GET":
            mbti_query_string = request.query_params.get("mbti", None)
            if mbti_query_string is None:
                return Post.objects.none()
            mbti_candidates = mbti_query_string.split(",")
            _filter = Q()
            for candidate in mbti_candidates:
                _filter |= Q(author__mbti__icontains=candidate)
            return queryset.filter(_filter)
        return queryset
