from django.contrib import admin
from .models import *


@admin.register(RoleModel)
class RoleModelAdmin(admin.ModelAdmin):
    list_display = ['id','name']


@admin.register(RegionModel)
class RegionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_user_id', 'fullname', 'phone','category']