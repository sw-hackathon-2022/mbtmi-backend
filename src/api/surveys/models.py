from django.db import models
from django.utils import timezone

from users.models import User


class Survey(models.Model):
    author = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    content = models.CharField(
        max_length=150
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = "survey"

    def __str__(self):
        return self.content


class SurveyItem(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE
    )
    content = models.CharField(
        max_length=100
    )

    class Meta:
        db_table = "survey_item"

    def __str__(self):
        return self.content


class SurveyReply(models.Model):
    replier = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        SurveyItem,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        db_table = "survey_reply"
        unique_together = ("replier", "item")

    def __str__(self):
        return f"{self.replier}님의 {self.item} 응답"
