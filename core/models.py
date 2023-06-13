from django.db import models
from userauths.models import User, Profile
from django.utils.html import mark_safe
# Create your models here.
from django.db import models
from shortuuid.django_fields import ShortUUIDField

class Page(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30, null=True)
    profile_pic=models.ImageField(upload_to='pages/profile_pictures/')
    cover_pic=models.ImageField(upload_to='pages/cover_pictures/')
    likes=models.IntegerField(default=0)
    about = models.TextField(null=True)
    class Meta:
        verbose_name_plural = "Pages"

    def page_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.profile_pic.url))

class LikedPage(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name_plural = "Liked Pages"
    def page_name(self):
        return self.page.name

class SharedPost(models.Model):
    spid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="spost", alphabet="abcdefgh12345", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    page=models.ForeignKey(Page, on_delete=models.CASCADE,null=True,blank=True)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    original_post_id = models.IntegerField(null=True)
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Shared_Posts"

class Posts(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    likes = models.IntegerField(null=True, default=0)
    comments = models.IntegerField(null=True, default=0)
    shares = models.IntegerField(null=True, default=0)
    shared_post = models.ForeignKey(SharedPost, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Posts"

    def post_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.image.url))
    
class General_information(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobbies = models.TextField(null=True, default="Not Added")
    education = models.TextField(null=True, default="Not Added")
    other_interests = models.TextField(null=True, default="Not Added")
    work_experience = models.TextField(null=True, default="Not Added")
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "General informations"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Likes"

class Comment(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="com", alphabet="abcdefgh12345", null=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post_comments")
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    image = models.ImageField(null=True)
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Comments"

class FriendRequest(models.Model):
    fri_req_id = ShortUUIDField(unique=True, length=10, max_length=30, prefix="fri_req", alphabet="abcdefgh12345", null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    sender_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='sent_friend_requests')
    reciever_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='recieve_friend_requests')
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    reciever_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recieve_friend_requests')
    is_friend = models.BooleanField(default=False)
    
    
    def sender_profile_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.sender_profile.profile_pic.url))
    
    def reciever_profile_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.reciever_profile.profile_pic.url))
    
    def sender_name(self):
        return self.sender_profile.firstname
    def reciever_name(self):
        return self.reciever_profile.firstname
    
    class Meta:
        verbose_name_plural = "Friend Requests"

class Friend(models.Model):
    fri_id = ShortUUIDField(unique=True, length=10, max_length=30, prefix="fri", alphabet="abcdefgh12345", null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True,related_name='user_friends')
    friend_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='friends')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_friends')
    friend_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='friends')

    
    def profile_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.profile.profile_pic.url))
    
    def friend_profile_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.friend_profile.profile_pic.url))
    
    def user_name(self):
        return self.profile.firstname
    def friend_name(self):
        return self.friend_profile.firstname

    class Meta:
        verbose_name_plural = "Friends"

class Story(models.Model):
    sid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="stry", alphabet="abcdefgh12345", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True)
    video = models.FileField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Stories"

class Notification(models.Model):
    nid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="not", alphabet="abcdefgh12345", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="sent_user")
    sent_to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="sent_profile")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True, blank=True)
    friends = models.BooleanField(default=False, blank=True)
    class Meta:
        verbose_name_plural = "Notifications"