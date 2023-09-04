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
    language = models.CharField(max_length=2, default='uz')
    rating_count = models.IntegerField(default=0)
    rating_stars = models.IntegerField(default=0)
    category = models.ForeignKey(CategoryModel, on_delete=models.RESTRICT)
    region = models.ForeignKey(RegionModel, on_delete=models.RESTRICT)
    role = models.ForeignKey(RoleModel, on_delete=models.RESTRICT)
