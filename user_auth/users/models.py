from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, first_name, last_name, email, password):
        if not email:
            raise ValueError("User must have enter email_id")
        user = self.model(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, password):
        if password is None:
            raise TypeError
        user = self.model(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.is_superuser = True
        user.verified = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=250, default=None)
    created_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','password']
    
    def __str__(self):
        return self.email
    
    