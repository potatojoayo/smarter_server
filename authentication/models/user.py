from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models

from authentication.managers.user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    identification = models.CharField(max_length=100, unique=True)
    fcm_token = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(null=True, upload_to='user/profile/')
    fcm_tokens = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    refund_account_no = models.CharField(max_length=50, null=True, blank=True)
    refund_account_bank = models.CharField(max_length=20, null=True, blank=True)
    refund_account_owner = models.CharField(max_length=10, null=True, blank=True)
    code_for_password = models.IntegerField(null=True, blank=True)
    code_limit_time = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_participated_event = models.BooleanField(default=False)
    USERNAME_FIELD = 'identification'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return '{}. {} - {} - {}'.format(self.id, self.name, self.identification, self.phone)





