from django.db import models

from reactions.models import BaseReaction


class Report(BaseReaction):
    reason = models.CharField(
        max_length=50,
    )

    class Meta:
        db_table = "report"

    def __str__(self):
        return f"{self.user}님의 {self.post} 신고"
