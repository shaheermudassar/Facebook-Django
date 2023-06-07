from django.contrib import admin
from userauths.models import User, Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'profile_image']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)