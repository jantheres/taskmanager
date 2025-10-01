from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager

class Roles(models.TextChoices):
    SUPERADMIN = 'SUPERADMIN', 'Super Admin'
    ADMIN = 'ADMIN', 'Admin'
    USER = 'USER', 'User'

class UserManager(DjangoUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', Roles.USER)
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', Roles.SUPERADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER
    )
    # For Users: which Admin manages them (nullable). Only meaningful if role=USER
    assigned_admin = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='managed_users',
        limit_choices_to={'role': Roles.ADMIN}
    )

    objects = UserManager()

    @property
    def is_superadmin(self):
        return self.role == Roles.SUPERADMIN

    @property
    def is_admin(self):
        return self.role == Roles.ADMIN

    @property
    def is_standard_user(self):
        return self.role == Roles.USER

    def __str__(self):
        return f'{self.username} ({self.role})'