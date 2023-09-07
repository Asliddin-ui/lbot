from django.db import models

from tgbot.decorators import i18n


@i18n
class RegionModel(models.Model):
    name_uz = models.CharField(max_length=255, default=None)
    name_ru = models.CharField(max_length=255, default=None)
    name_en = models.CharField(max_length=255, default=None)


@i18n
class RoleModel(models.Model):
    name_uz = models.CharField(max_length=255, default=None)
    name_ru = models.CharField(max_length=255, default=None)
    name_en = models.CharField(max_length=255, default=None)


@i18n
class CategoryModel(models.Model):
    name_uz = models.CharField(max_length=255, default=None, blank=True)
    name_ru = models.CharField(max_length=255, default=None, blank=True)
    name_en = models.CharField(max_length=255, default=None, blank=True)


class TelegramUser(models.Model):
    telegram_user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255, default=None, blank=True, null=True)
    fullname = models.CharField(max_length=255, default=None, blank=True, null=True)
    phone = models.CharField(max_length=12, default=None, unique=True)
    language = models.CharField(max_length=2, default='uz', null=True, blank=True)
    rating_count = models.IntegerField(default=0)
    rating_stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(CategoryModel),
    region = models.ForeignKey(RegionModel, on_delete=models.RESTRICT, default=1)
    role = models.ForeignKey(RoleModel, on_delete=models.RESTRICT, default=None, null=True)
