from django.db import models
from django.contrib.auth.models import User
from chat_app.storage import OverwriteStorage
import os
# chat room model
class Chat(models.Model):
    name = models.CharField(max_length=30 )
    users = models.ManyToManyField(User)
    type = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

#message model
class Message(models.Model):
    username = models.ForeignKey(User)
    timestamp = models.DateTimeField()
    message = models.CharField(max_length=900)
    chat = models.ForeignKey(Chat)

    def __unicode__(self):
        return self.username.username

# function to create a path of a image for a user profile
def get_upload_file_name(instance,filename):
    return 'profile_pictures/%d/%s.jpg' % (int(instance.user_id), instance.user.username)
# model to store a image for a user
class UserProfilePic(models.Model):
    user = models.OneToOneField(User)
    pic=models.ImageField(upload_to = get_upload_file_name, blank=True , null=True, storage=OverwriteStorage())

    def __unicode__(self):
        return self.user.username

User.profile = property(lambda u:UserProfilePic.objects.get_or_create(user=u)[0])