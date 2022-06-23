from django.db import models
from django.utils import timezone

from users.models import User


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=50
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        db_table = "post"

    def __str__(self):
        return self.title
