from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile (models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profpic = models.ImageField(upload_to='profpic/', blank=True, default=False)

    bio = models.TextField(max_length=500, blank=True)

    gender = models.CharField(max_length=30, blank= True)

    def __str__(self):

        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:

        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    instance.profile.save()


class Post(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, null=True)

    image = models.ImageField(upload_to='post/', blank=True, default=False)

    caption = models.CharField(max_length=250, blank=True)

    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user.username

    class Meta:

        ordering = ['-post_date']


