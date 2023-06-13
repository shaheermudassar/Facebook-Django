from django.shortcuts import render, redirect
from userauths.models import *
from core.models import FriendRequest
from core.models import *

def default(request):
    profile_pro = None
    profile_path = None
    friend_requests_count = None
    notifications_count = None
    notifications = None
    friends = None
    if request.user.is_authenticated and Friend.objects.filter(user=request.user).exists():
        friends=Friend.objects.filter(user=request.user)
    if request.user.is_authenticated and Profile.objects.filter(user=request.user).exists():
        profile_pro = Profile.objects.get(user = request.user)
        profile_path = f"/profile/{profile_pro.user.id}/"
    if request.user.is_authenticated and FriendRequest.objects.filter(reciever_user = request.user).exists():
        friend_requests_count = FriendRequest.objects.filter(reciever_user = request.user).count()
    if request.user.is_authenticated and Notification.objects.filter(sent_to=request.user).exists():
        notifications =Notification.objects.filter(sent_to=request.user).order_by("-id")
        notifications_count = Notification.objects.filter(sent_to=request.user, seen=False).count()
    return{
        "profile_pro": profile_pro,
        "friend_requests_count": friend_requests_count,
        "profile_path": profile_path,
        "notifications": notifications,
        "notifications_count": notifications_count,
        "friends":friends,
    }