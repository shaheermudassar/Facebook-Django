from django.db import models
from userauths.models import User, Profile
from django.utils.html import mark_safe
# Create your models here.
from django.db import models
from shortuuid.django_fields import ShortUUIDField

# Create your models here.
class Message(models.Model):
    mid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="msg", alphabet="abcdefgh12345", null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    sender_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True,related_name='sender_profile')
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender_user')
    reciever_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='reciever_profile')
    reciever_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='reciever_user')
    sender_body = models.TextField(null=True, blank=True)
    reciever_body = models.TextField(null=True, blank=True)

    def sender_profile_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.sender_profile.profile_pic.url))
    
    def reciever_profile_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.reciever_profile.profile_pic.url))
    
    def sender_name(self):
        return self.sender_profile.firstname
    def reciever_name(self):
        return self.reciever_profile.firstname
    class Meta:
        verbose_name_plural = "Messages"