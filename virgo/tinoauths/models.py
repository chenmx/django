# encoding: utf-8

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import hashlib

class UserManager(BaseUserManager):

    def create_user(self, imei, idfa, open_udid):

        user = self.model(
            imei=imei,
            idfa=idfa,
            open_udid=open_udid,
        )
        # user.uid = hashlib.md5(imei+idfa+open_udid).hexdigest()
        # user.name = hashlib.md5(imei).hexdigest()

        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):

        user = self.create_user(name, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''用户表'''

    name = models.CharField(max_length=100)#, unique=True)
    email = models.EmailField(max_length=100)
    avatar = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    imei = models.CharField(max_length=100, unique=True)
    idfa = models.CharField(max_length=100, unique=True)
    open_udid = models.CharField(max_length=100, unique=True)
    uid = models.CharField(max_length=200, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ()

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.name

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
