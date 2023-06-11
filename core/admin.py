from django.contrib import admin
from core.models import Posts, General_information, Like, Comment, SharedPost, Friend, FriendRequest, Story

# Register your models here.
class PostsAdmin(admin.ModelAdmin):
    list_display = ['user', 'content']

class General_informationAdmin(admin.ModelAdmin):
    list_display = ['user']

class LikeAdmin(admin.ModelAdmin):
    list_display = ['user']

class FriendAdmin(admin.ModelAdmin):
    list_display = ["friend_profile_image","profile_image", 'user_name', 'friend_name']
    # list_display = ['user']
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender_name',"sender_profile_image","reciever_profile_image",  "reciever_name"]
    # list_display = ['send_user']
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', "comment"]

class SharedPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

class StoriesAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile', 'created_at']

admin.site.register(Posts, PostsAdmin)
admin.site.register(SharedPost, SharedPostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Story, StoriesAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(General_information, General_informationAdmin)