from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User,related_name="profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    phone = models.DecimalField(max_digits=10, decimal_places=0,null=True, blank=True)
    picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, blank=True, help_text='The MIMEType of the file')
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
    ask= models.DecimalField(max_digits=1, decimal_places=0,blank=True,null=True)

    def __str__(self):
        return str(self.topic)

    # def add_options(self, options):
    #     if self.options_set.count() >= 12:
    #          raise Exception(f'{self.forum.topic} can have maximum 4 options. No more allowed.')

    #     self.forum_set.add(options)

class options(models.Model):
    option_access=models.ForeignKey(forum,on_delete=models.CASCADE,related_name="option_access")
    option=models.CharField(max_length=300,blank=True,null=True)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if self.options_set.count() < 5:
    #         super(options, self).save()
    #     else:
    #         raise Exception(f'{self.forum.topic} can have maximum 4 options. No more allowed.')

class forum_tags(models.Model):

    tags_access=models.ForeignKey(forum,on_delete=models.CASCADE,related_name="tag_access")
    tags_forum=models.CharField(max_length=50,blank=True,null=True)

#child model
class Discussion(models.Model):
    forum = models.ForeignKey(forum,blank=True,on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
    single = models.CharField(max_length=50,blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.forum)
