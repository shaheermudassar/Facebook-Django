from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.html import mark_safe

GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

class User(AbstractUser):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=100)
    bio=models.CharField(max_length=255)
    is_vendor = models.BooleanField(null=True, default=False)
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    firstname=models.CharField(max_length=25, null=True)
    lastname=models.CharField(max_length=25, null=True)
    bio=models.TextField(null=True)
    city=models.CharField(max_length=100, null=True)
    country=models.CharField(max_length=100, null=True)
    gender=models.CharField(max_length=100, choices=GENDER_CHOICES)
    profile_pic=models.ImageField(upload_to='profile_pictures/')
    cover_pic=models.ImageField(upload_to='cover_pictures/')
    birthday = models.DateField(null=True)
    phone_no = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.firstname
    
    class Meta:
        verbose_name_plural = "Profiles"

    def profile_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>'% (self.profile_pic.url))
    
