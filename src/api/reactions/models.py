from django.db import models

# Create your models here.
from django.utils import timezone

from posts.models import Post
from users.models import User


class BaseReaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        abstract = True


class Like(BaseException):
    class Meta:
        db_table = "like"

    def __str__(self):
        return f"{self.user}님이 {self.post}에 공감합니다."


class Unlike(BaseException):
    class Meta:
        db_table = "unlike"

    def __str__(self):
        return f"{self.user}님이 {self.post}에 바공감합니다."
