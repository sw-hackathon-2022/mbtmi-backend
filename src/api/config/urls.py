from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # api docs
    path("docs/schema/", SpectacularJSONAPIView.as_view(), name="docs"),  # api documentation file
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="docs"), name="swagger"),  # api docs by swagger
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="docs"), name="redoc"),  # api docs by redoc
    # apps
    path("posts/", include("posts.urls")),
    path("posts/<int:post_id>/", include("reactions.urls")),
    path("posts/<int:post_id>/comments", include("comments.urls")),
    path("users/", include("users.urls")),
    path("surveys/", include("surveys.urls")),
    path("reports/", include("reports.urls")),
]
