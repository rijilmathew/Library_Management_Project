from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('regular', 'Regular User'),
        ('staff', 'Staff User'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='regular')
    
    def is_staff_user(self):
        return self.role == 'staff'


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    

    def __str__(self):
        return self.user.username