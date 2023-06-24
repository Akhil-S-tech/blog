from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    username=models.CharField(max_length=20,unique=True)
    email=models.EmailField(max_length=255,unique=True)
    avatar=models.ImageField(upload_to="profile/",default="media/avatar.jpg")
    bio=models.TextField(blank=True)

    def __str__(self):
        return self.username




