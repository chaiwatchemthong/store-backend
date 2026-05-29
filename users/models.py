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

class User(AbstractBaseUser):
    ROLE_CHOICES = [('seller', 'Seller'), ('buyer', 'Buyer')]

    email      = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.email} ({self.role})'
