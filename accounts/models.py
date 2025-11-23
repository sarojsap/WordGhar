from django.db import models
from django.contrib.auth.models import AbstractUser

def user_profile_photo_path(instance, filename):
    """Generate path for user profile photos"""
    return f'profile_photos/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, help_text="A short bio about yourself")
    profile_photo = models.ImageField(upload_to=user_profile_photo_path, blank=True, null=True, help_text="Your profile photo")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Your date of birth")
    
    def __str__(self):
        return self.username