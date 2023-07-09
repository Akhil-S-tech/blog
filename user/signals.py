from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

USER = get_user_model()


# When any user register or created immediately create a profile table for that user.
@receiver(post_save, sender=USER)
def create_user(sender, instance, created, *args, **kwargs):
    profile = Profile()
    user = instance
    if created:
        profile.user = user
        profile.username = user.username
        profile.name = user.name
        profile.email = user.email
        profile.save()


# When the profile is updated that time the user column also updated.
@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, *args, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.username = profile.username
        user.name = profile.name
        user.email = profile.email
        user.save()


@receiver(pre_save, sender=Profile)
def profile_pre_save(sender, instance, *args, **kwargs):
    instance.username = instance.username.lower()


@receiver(pre_save, sender=USER)
def user_pre_save(sender, instance, *args, **kwargs):
    instance.username = instance.username.lower()
