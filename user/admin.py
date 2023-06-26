from django.contrib import admin
from .models import Profile,User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['username','name','email']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['username','name','email','avatar']
  