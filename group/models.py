from django.db import models
from user.models import User
from asgiref.sync import sync_to_async

from django.db import models



class Group(models.Model):
    title = models.CharField(max_length=50, verbose_name='نام گروه')
    users_name = models.CharField(max_length=50, verbose_name='نام بچه های گروه', blank=True, null=True)
    chat_id = models.IntegerField(verbose_name='id گروه')
    created = models.DateField(auto_now_add=True, verbose_name='زمان اضافه شدن بات')
    users = models.ManyToManyField(User, verbose_name='کاربران گروه', blank=True)
    users_to_make_group = models.ManyToManyField(User, verbose_name='کاربران برای گروه بندی', blank=True, related_name='user_to_make_group')
    is_active = models.BooleanField(default=False, verbose_name='گروه جامعه ی شیراز')
    def __str__(self):
        return self.title

    async def get(self, *attrs):
        if len(attrs) == 1:
            return getattr(self, attrs[0], None)
        else:
            return tuple(getattr(self, attr, None) for attr in attrs)

    class Meta:
        verbose_name = 'گروه'
        verbose_name_plural = "گروه ها"

class UserCategory(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='نام دسته بندی ')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='گروه')
    users = models.ManyToManyField(User, verbose_name='کاربران')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'دسته بندی بجه های گروه'
        verbose_name_plural = "دسته بندی های بجه های گروه"

    async def get(self, *attrs):
        if len(attrs) == 1:
            return getattr(self, attrs[0], None)
        else:
            return tuple(getattr(self, attr, None) for attr in attrs)







