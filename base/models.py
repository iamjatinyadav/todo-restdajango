from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
# Create your models here.
# from django.contrib.auth.models import PermissionsMixin

import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff = False, is_admin = False):
        if not email:
            raise ValueError("user must have a email address")
        if not password:
            raise ValueError("user must have a password")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, email, password=None):
        user = self.create_user(
            email,
            password = password,
            is_staff=True
            )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    age = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin


class TodoItems(models.Model):
    class Status(models.IntegerChoices):
        NotStarted = 0
        OnGoing = 1
        Completed = 2
    name = models.CharField(max_length=255)
    Description = models.TextField(max_length=300, null=True, blank=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="todoitems")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=Status.choices, default=Status.NotStarted)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'TodoItem'
        verbose_name_plural = 'TodoItems'

