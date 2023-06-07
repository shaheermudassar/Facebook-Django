from django.shortcuts import render, redirect
from userauths.models import Profile, User
from core.models import Like

def default(request):
    profile_pro = None
    if request.user.is_authenticated:
        profile_pro = Profile.objects.get(user = request.user)
    return{
        "profile_pro": profile_pro,
    }