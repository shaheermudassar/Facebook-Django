from django.urls import path, include
from core import views

app_name = 'core'

urlpatterns = [
    path("", views.newsfeed ,name="newsfeed"),
    path("profile/<id>", views.profile ,name="profile"),
    path("settings", views.edit_account ,name="settings"),
    path("like/", views.like ,name="like"),
    path("share_post/", views.share_post ,name="share_post"),
    path("create-profile", views.create_profile ,name="create-profile"),
    path("post/<id>", views.post_details ,name="post"),
    path("videos", views.videos ,name="videos"),
]
