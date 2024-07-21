from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None):
        if not user_id:
            raise ValueError("Users must have an user id ")

        user = self.model(
            user_id=user_id,
        )
        if not user.username:
            user.username = user.user_id
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            password=password,
            user_id=user_id,
        )
        user.is_admin = True
        if not user.username:
            user.username = user.user_id
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.IntegerField(verbose_name='id عددی', primary_key=True, unique=True)
    username = models.CharField(max_length=40,  verbose_name='یوزرنیم تلگرام', blank=True, null=True)
    name = models.CharField(max_length=40, verbose_name='نام', blank=True, null=True, help_text='این فیلد توسط بات بر اساس نام تلگرام پر میشود')
    real_name = models.CharField(max_length=100, verbose_name='نام کامل', help_text='این فیلد توسط کاربر پر میشود', null=True, blank=True)
    is_dev = models.BooleanField(default=False, verbose_name='توسعه دهنده')
    is_main_admin = models.BooleanField(default=True, verbose_name='ادمین تمام')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    instagram_id = models.CharField(max_length=60, blank=True, null=True)
    number = models.CharField(max_length=60, blank=True, null=True)
    objects = UserManager()
    message_count = models.PositiveIntegerField(default=0)
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


    def __str__(self):
        if self.name:
            return self.name
        elif self.username:
            return self.username
        else:
            return str(self.user_id)
    def has_perm(self, perm, obj=None):
        "permission"
        return True

    def has_module_perms(self, app_label):
        " user have permissions to view the app"
        return True
    def role(self):
        if self.is_admin:
            return 'admin'
        else:
            return 'user'

    @property
    def is_staff(self):
        # Is the user a member of staff ?
        return self.is_admin

    async def get(self, *attrs):
        if len(attrs) == 1:
            return getattr(self, attrs[0], None)
        else:
            return tuple(getattr(self, attr, None) for attr in attrs)