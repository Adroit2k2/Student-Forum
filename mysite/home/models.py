from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db.models.query import QuerySet



class Profile(models.Model):
    user = models.OneToOneField(User,related_name="profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    phone = models.DecimalField(max_digits=10, decimal_places=0,null=True, blank=True)
    picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, blank=True, help_text='The MIMEType of the file')
    bio = models.TextField()
    github_link = models.URLField(max_length = 200, blank=True, null=True, default='http://null.html', editable=True)
    linkedin_link = models.URLField(max_length = 200, blank=True, null=True, default='http://null.html', editable=True)

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
    updated_at = models.DateTimeField(auto_now=True,null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type_code= models.CharField(max_length=1,default=3)
    ask= models.DecimalField(max_digits=1, decimal_places=0,blank=True,null=True)
    total=models.IntegerField(null=True,blank=True,default=0)
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,through='Fav', related_name='favorite')
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
    # tags_forum=CollectionField(max_items=5,sort=True,blank=True,null=True,unique_items=True,delimiter='|',max_length=50)

#child model
class Discussion(models.Model):
    forum = models.ForeignKey(forum,blank=True,on_delete=models.CASCADE,related_name="discuss_access")
    discuss = models.CharField(max_length=1000)
    single = models.CharField(max_length=100,blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.forum)

class Vote(models.Model):

    class Meta:
        unique_together = (('userprofile','answer'),)

    userprofile = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="vivekmc",on_delete=models.CASCADE)
    answer= models.ForeignKey(forum, related_name="anshumc" ,on_delete=models.CASCADE)
    votes=models.IntegerField(null=True,blank=True,default=0)

class Fav(models.Model) :
    forum_fav = models.ForeignKey(forum, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('forum_fav', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.forum_fav.topic[:10])
