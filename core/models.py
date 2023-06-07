from django.db import models
from userauths.models import User, Profile
from django.utils.html import mark_safe
# Create your models here.
from django.db import models
from shortuuid.django_fields import ShortUUIDField

class SharedPost(models.Model):
    spid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="spost", alphabet="abcdefgh12345", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    likes = models.IntegerField(null=True, default=0)
    comments = models.IntegerField(null=True, default=0)
    shares = models.IntegerField(null=True, default=0)
    shared_post = models.ForeignKey(SharedPost, on_delete=models.CASCADE, null=True)

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
        verbose_name_plural = "General_informations"

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