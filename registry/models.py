from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django_jalali.db import models as jmodels
from datetime import timedelta
import random


def get_random_string(length=5):
    # put your letters in the following string
    sample_letters = '1234567890'
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))
    return result_str


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password, mobile_number=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.mobile_number = mobile_number
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, mobile_number=None):
        user = self.create_user(
            username=username,
            email=email,
            mobile_number=mobile_number,
            password=password,

        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    avatar = models.ForeignKey("Avatar", on_delete=models.SET_NULL, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.username


class Avatar(models.Model):
    avatar = models.ImageField(upload_to="avatars/")
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
