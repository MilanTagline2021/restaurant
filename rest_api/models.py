from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = False
        user.save(using=self._db)
        return user


class User(AbstractUser):
    USER_TYPE = (
        ('restaurant_owner', 'restaurant_owner'),
        ('customer', 'customer'),
        ('admin', 'admin')
    )
    username = None
    full_name = models.CharField(max_length=255, verbose_name="Name")
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE, default='customer')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
