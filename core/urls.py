from django.urls import path, include
from core import views

app_name = 'core'

urlpatterns = [
    path("", views.newsfeed ,name="newsfeed"),
    path("profile/<id>/", views.profile ,name="profile"),
    path("settings/", views.edit_account ,name="settings"),
    path("like/", views.like ,name="like"),
    path("share_post/", views.share_post ,name="share_post"),
    path("create-profile/", views.create_profile ,name="create-profile"),
    path("post/<id>/", views.post_details ,name="post"),
    path("page/<id>/", views.page ,name="page"),
    path("edit-page/<id>/", views.edit_page ,name="edit-page"),
    path("create-page/", views.create_page ,name="create-page"),
    path("videos/", views.videos ,name="videos"),
    path("friend-requests/", views.friend_requests ,name="friend-requests"),
    path("delete_friend_request/", views.delete_friend_request ,name="delete_friend_request"),
    path("accept_friend_request/", views.accept_friend_request ,name="accept_friend_request"),
    path("user-pages/", views.user_pages ,name="user-pages"),
    path("all-users/", views.all_users ,name="all-users"),
    path("liked_pages/", views.liked_pages ,name="liked_pages"),
    path("all-pages/", views.all_pages ,name="all-pages"),
    path("search/", views.search ,name="search"),
    path("notifications/", views.notifications ,name="notifications"),
]
