from django.db.models import Q
from rest_framework import filters
from rest_framework.request import Request


class PostByMBTIFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset, view):
        mbti_candidates = request.query_params.get("mbti").split(",")  #
        _filter = Q()
        for candidate in mbti_candidates:
            _filter |= Q(author__mbti=candidate)
        queryset.filter(_filter)
        return queryset.filter(queryset)
