from django.db import models
from django.utils import timezone

from posts.models import Post
from users.models import User


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    content = models.CharField(
        max_length=300
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        db_table = "comment"

    def __str__(self):
        return f"[{self.post}] {self.content}"
