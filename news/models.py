from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        unique=True,
        on_delete=models.CASCADE
    )
    bio = models.TextField(max_length=500, blank=True, null=True)
    vk_page = models.CharField(verbose_name='Страница Вконтакте',max_length=30,blank=True, null=True)
    rate = models.FloatField(verbose_name='Рейтинг', default=1000.0)
    
    def __str__(self):
        return self.user.username
    
        
 
@receiver(post_save, sender=User)    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
      
 
@receiver(post_save, sender=User)    
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
 # @receiver(post_save, sender=User, dispatch_uid='myproject.myapp.models.user_post_save_handler')
 # def user_post_save(sender, instance, created, **kwargs):
 #   if created:
 #      instance.groups.add(Group.objects.get(name='Пользователи')) 
