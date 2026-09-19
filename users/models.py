import random
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager 

def generate_code():
    return str(random.randint(100000, 999999))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return self.email or ""
    

class ConfirmCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='confirm_code')
    code = models.CharField(max_length=6, default=generate_code)

    def __str__(self):
        return f'{self.user.username} - {self.code}'


