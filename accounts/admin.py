from django.contrib import admin

from models import UserFollow, UserProfile

class UserFollowAdmin(admin.ModelAdmin):
    list_display=['user', 'followed_user']

class UserProfileAdmin(admin.ModelAdmin):
    list_display=['user', 'location', 'url', 'profile_privacy']

admin.site.register(UserFollow, UserFollowAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
