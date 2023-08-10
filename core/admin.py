from django.contrib import admin
from core.models import *

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
    list_display = ['sender_name',"sender_profile_image","reciever_profile_image", "is_friend",  "reciever_name"]
    list_editable = ["is_friend"]
    # list_display = ['send_user']
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', "comment"]

class SharedPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

class StoriesAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile', 'created_at']

class PagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'page_image', 'created_at']

class LikedPagesAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'user']

class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['sent_to', 'body']

admin.site.register(Posts, PostsAdmin)
admin.site.register(SharedPost, SharedPostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Story, StoriesAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(General_information, General_informationAdmin)
admin.site.register(Page, PagesAdmin)
admin.site.register(LikedPage, LikedPagesAdmin)
admin.site.register(Notification, NotificationsAdmin)