from django.contrib import admin
from chat_app.models import Message,Chat,UserProfilePic

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(UserProfilePic)