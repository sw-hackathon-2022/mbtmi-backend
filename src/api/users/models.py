from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):

    MBTI_CHOICES = (
        ("XXXX", "XXXX"),
        ("ISTJ", "ISTJ"),
        ("ISTP", "ISTP"),
        ("ISFJ", "ISFJ"),
        ("INTJ", "INTJ"),
        ("ESTJ", "ESTJ"),
        ("ISFP", "ISFP"),
        ("INFJ", "INFJ"),
        ("ESFJ", "ESFJ"),
        ("ESFP", "ESFP"),
        ("INFP", "INFP"),
        ("INTP", "INTP"),
        ("ESTP", "ESTP"),
        ("ENTJ", "ENTJ"),
        ("ENTP", "ENTP"),
        ("ENFP", "ENFP"),
        ("ENFJ", "ENFJ"),
    )

    mbti = models.CharField(
        max_length=4,
        default="XXXX",
        choices=MBTI_CHOICES
    )
    email = models.EmailField(
        max_length=30,
        null=True,
        blank=True,
    )
    username = models.BigIntegerField(
        unique=True,
    )
    password = models.CharField(
        max_length=50
    )
    about = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"{self.username}"
