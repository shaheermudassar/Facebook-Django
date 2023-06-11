from django.contrib import admin
from messenger.models import Message

# Register your models here.
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['sender_name',"sender_profile_image","reciever_profile_image",  "reciever_name"]

admin.site.register(Message, MessagesAdmin)