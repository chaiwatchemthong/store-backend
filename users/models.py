from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password, role='buyer', **extra):
        if not email:
            raise ValueError('Email required')
        user = self.model(email=self.normalize_email(email), role=role, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra):  # ← เพิ่ม
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, password, role='buyer', **extra)

class User(AbstractBaseUser, PermissionsMixin):  # ← เพิ่ม PermissionsMixin
    ROLE_CHOICES = [('seller', 'Seller'), ('buyer', 'Buyer')]

    email      = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    is_staff   = models.BooleanField(default=False)   # ← เพิ่ม
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.email} ({self.role})'