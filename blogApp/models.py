from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING
#import django signal package
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.name)

class Post(models.Model):
    post_image = models.FileField(blank=True,null=True,upload_to="img/")
    heading = models.CharField(max_length=100)
    post_string = models.CharField(max_length=8)
    description = models.TextField(max_length=500)
    author = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    category_id = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.heading)

class Comments(models.Model):
    comment_text = models.TextField(max_length=200)
    post_id = models.ForeignKey(to=Post, on_delete=DO_NOTHING)
    user_name = models.CharField(max_length=100, null=True,default='Mike')
    user_profile = models.CharField(default="users-profiles/default-avatar.png",max_length=120, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.comment_text)

class PostView(models.Model):
    post_id = models.ForeignKey(to=Post, on_delete=DO_NOTHING)
    post_url = models.CharField(max_length=25, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.post_id)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    image_profile = models.ImageField(default="users-profiles/default-avatar.png" ,blank=True,null=True,upload_to="img/users-profiles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

#connecting the reciever to the sender(trigger)

# post_save.connect(create_profile,sender=User)
@receiver(post_save,sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.profile.save()
        print('user profile updated')
# post_save.connect(update_profile,sender=User)

# def create_user_profile(sender, instance, created, **kwargs):
#     try:
#         instance.profile.save()
#     except ObjectDoesNotExist:
#         Profile.objects.create(user=instance)




