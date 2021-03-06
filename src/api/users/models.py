from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, about, mbti="XXXX", password=None, email=None):
        user = self.model(
            mbti=mbti,
            username=int(username),
            about=about,
            email=self.normalize_email(email),
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, about=None, mbti="XXXX", password=None, email=None):
        user = self.create_user(
            mbti=mbti,
            username=username,
            about=about,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


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

    objects = UserManager()

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
    username = models.CharField(
        max_length=10,
        unique=True,
    )
    password = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    about = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["mbti",]

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"[#{self.id}] {self.username}"

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """Always has perms"""
        return True

    def has_module_perms(self, app_label):
        """Always has module perms"""
        return True

    def get_shortten_username(self):
        return self.username[-4:]
