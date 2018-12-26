from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

from django.conf import settings
# Create your models here.

class UserProfileManager(BaseUserManager):
    # help django work with our custom user models

    def create_user(self,email,name,password=None):
        # create a new user object

        if not email:
            raise ValueError('Email Field is required')

        email = self.normalize_email(email)
        user = self.model(email=email,name=name)
        user.set_password(password)
        user.save(using = self.db)

        return user

    def create_superuser(self,email,name,password):
        # create and save the new super user
        user = self.create_user(email,name,password)
        user.is_super_user = True
        user.is_staff = True

        user.save(using=self.db)
        return user

class UserProfile(AbstractBaseUser):
    # ---Represent user profiles into our system---

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # use to get user full name

        return self.name

    def get_short_name(self):
        # use to get short name of UserProfile

        return self.name

    def ___str___(self):
        # use to print full profile of user

        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

class ProfileFeedItem(models.Model):
    # profile status Update

    user_profile = models.ForeignKey("UserProfile", null=True, default=None, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text
