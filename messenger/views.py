from django.shortcuts import render, redirect
from core.models import Posts, General_information, Like, Comment, SharedPost, FriendRequest, Friend, Story
from userauths.models import Profile, User
from messenger.models import Message
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Random
from django.db.models import Q, F

# Create your views here.
def messenger(request):
    recent = None
    if Friend.objects.filter(user=request.user).exists():
        recent = Friend.objects.filter(user=request.user)
    context = {
        "recent": recent,
    }

    return render(request, "messenger/messenger.html", context)

def chat(request, id):
    user = User.objects.get(id=id)
    friend_profile = Profile.objects.get(user=user)
    reciever_profile = Profile.objects.get(user=user)
    sender_profile = Profile.objects.get(user=request.user)
    recent = None
    messages = None

    if Message.objects.filter(reciever_user=user, sender_user=request.user).exists():
        messages = Message.objects.filter(reciever_user=user, sender_user=request.user)
    
    if request.method == "POST":
        if "send_message" in request.POST:
            sender_body = request.POST.get("sender_body")
            Message.objects.create(
                sender_user=request.user,
                sender_profile=sender_profile,
                reciever_user=user,
                reciever_profile=reciever_profile,
                sender_body=sender_body,
            )
            Message.objects.create(
                sender_user=user,
                sender_profile=reciever_profile,
                reciever_user=request.user,
                reciever_profile=sender_profile,
                reciever_body=sender_body,
            )
            return redirect("messenger:chat", id)
        elif "delete_message" in request.POST:
            mid = request.POST.get("mid")
            delete_message = Message.objects.get(mid=mid)
            delete_message.delete()
            return redirect("messenger:chat", id)
    context = {
        "messages": messages,
        "user": user,
        "friend_profile": friend_profile,
    }
    return render(request, "messenger/chatroom.html", context)

def search(request):
    query = request.GET.get("query")
    recents = None
    if query:
        terms = query.split()
        queries = [Q(firstname__icontains=term) | Q(lastname__icontains=term) | Q(user__username__icontains=term) for term in terms]
        recents = Profile.objects.filter(*queries)
    context = {
        "recent": recents,
    }
    return render(request, "messenger/search.html", context)

