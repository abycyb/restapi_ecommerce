import datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework.exceptions import NotAcceptable
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserProfile(models.Model):    
    ROLE_CHOICES = [
        ('OWNER', 'owner'),
        ('SUPERVISOR', 'supervisor'),
        ('CUSTOMER', 'customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserProfile')
    role = models.CharField(max_length = 30, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to='userimg', blank=True, null=True, default=None)      

    def __str__(self):
        return self.user.get_full_name()