from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



# Create your models here.
# class all_tags(models.Model):
#         tag_all=models.ForeignKey(forum_tags,on_delete=models.CASCADE,related_name="all_tag")

class forum(models.Model):

    topic= models.CharField(max_length=300)
    description = models.CharField(max_length=1000,blank=True)
    link = models.CharField(max_length=100 ,null =True,default="null")
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type_code= models.CharField(max_length=1,default=3)


    def __str__(self):
        return str(self.topic)

class options(models.Model):
    option_access=models.ForeignKey(forum,on_delete=models.CASCADE,related_name="acesss")
    option=models.CharField(max_length=300)
class forum_tags(models.Model):

    tags_access=models.ForeignKey(forum,on_delete=models.CASCADE,related_name="access")
    tags_forum=models.CharField(max_length=50)

#child model
class Discussion(models.Model):
    forum = models.ForeignKey(forum,blank=True,on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
    single = models.CharField(max_length=50,blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.forum)
