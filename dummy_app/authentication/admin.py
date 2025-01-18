from django.contrib import admin
from authentication.models import User
from authentication.models import UserFollows


class UserModelAdmin(admin.ModelAdmin):
    list_display = ["username", ]


class UserFollowsModelAdmin(admin.ModelAdmin):
    list_display = ["user", "followed_user", ]


admin.site.register(User, UserModelAdmin)
admin.site.register(UserFollows, UserFollowsModelAdmin)
