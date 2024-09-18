from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('regular', 'Regular User'),
        ('staff', 'Staff User'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='regular')
    
    def is_staff_user(self):
        return self.role == 'staff'
