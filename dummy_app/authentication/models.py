from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    ADMIN = "ADMIN"
    USER = "USER"
    ROLES_SET = (
        (ADMIN, "administrateur"),
        (USER, "utilisateur"),
    )
    role = models.CharField(max_length=15, choices=ROLES_SET, default=ROLES_SET[1][0], verbose_name="role")
    abonnements = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="UserFollows",
        related_name="user",
    )

    def _update_follower(self, user):
        user_follow = UserFollows(user=user, followed_user=user)
        user_follow.save()

    def __save__(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        self._update_follower(user)

    def __str__(self):
        return f"{self.username}"


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE, )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, related_name='followed_by', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'followed_user', )
