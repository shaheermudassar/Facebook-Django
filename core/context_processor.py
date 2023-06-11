from django.shortcuts import render, redirect
from userauths.models import Profile, User
from core.models import FriendRequest
from core.models import Like

def default(request):
    profile_pro = None
    friend_requests_count = None
    if request.user.is_authenticated and Profile.objects.filter(user=request.user).exists():
        profile_pro = Profile.objects.get(user = request.user)
    if request.user.is_authenticated and FriendRequest.objects.filter(reciever_user = request.user).exists():
        friend_requests_count = FriendRequest.objects.filter(reciever_user = request.user).count()
    return{
        "profile_pro": profile_pro,
        "friend_requests_count": friend_requests_count,
    }