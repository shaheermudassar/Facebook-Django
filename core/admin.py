from django.contrib import admin
from core.models import Posts, General_information, Like, Comment, SharedPost

# Register your models here.
class PostsAdmin(admin.ModelAdmin):
    list_display = ['user', 'content']

class General_informationAdmin(admin.ModelAdmin):
    list_display = ['user']

class LikeAdmin(admin.ModelAdmin):
    list_display = ['user']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', "comment"]

class SharedPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

admin.site.register(Posts, PostsAdmin)
admin.site.register(SharedPost, SharedPostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(General_information, General_informationAdmin)