from django.conf import settings
from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from django.utils.translation import gettext as _
from telegram.ext import ContextTypes

from tgbot.models import CategoryModel, RegionModel, RoleModel, MenuModel


async def lang_button():
    buttons = []
    for lang in settings.LANGUAGES:
        buttons.append(InlineKeyboardButton(
            f'{lang[1]}', callback_data=f'{lang[0]}'
        ))
        print(lang[0])
    return InlineKeyboardMarkup([buttons[i:i + 2] for i in range(0, len(buttons), 2)])


async def get_contact():
    button = [
        [KeyboardButton(_('Raqamni jo`natish'), request_contact=True)]
    ]
    return ReplyKeyboardMarkup(button, resize_keyboard=True)


async def region_button():
    button = []
    async for region in RegionModel.objects.order_by('-id').all():
        button.append(
            InlineKeyboardButton(region.name, callback_data=region.id)
        )
    return InlineKeyboardMarkup([button[i:i + 2] for i in range(0, len(button), 2)])


async def get_role():
    button = []
    async for role in RoleModel.objects.order_by('-id').all():
        button.append(
            InlineKeyboardButton(role.name, callback_data=role.id)
        )
    return InlineKeyboardMarkup([button[i:i + 2] for i in range(0, len(button), 2)])


async def category_button(context: ContextTypes.DEFAULT_TYPE):
    button = []
    selected_jobs = context.user_data['category']
    async for cat in CategoryModel.objects.order_by('-id').exclude(id__in=selected_jobs).all():
        button.append(
            InlineKeyboardButton(cat.name, callback_data=cat.id)
        )
    return InlineKeyboardMarkup([button[i:i + 2] for i in range(0, len(button), 2)])


async def yes_no_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton('Yes', callback_data='yes'),
                                  InlineKeyboardButton('No', callback_data='no')]])


async def get_menu():
    button = []

    async for menu in MenuModel.objects.order_by('-id').all():
        if menu.parent_id is None:
            button.append(
                KeyboardButton(menu.name)
            )
    return ReplyKeyboardMarkup(([button[i:i + 2] for i in range(0, len(button), 2)]), resize_keyboard=True)


async def get_menus(msg):
    button = []
    async for menu in MenuModel.objects.filter(name=msg).all():
        button.append(
            InlineKeyboardButton(menu.name, callback_data=f"menu_{menu.id}")
        )
    return InlineKeyboardMarkup([button[i:i + 2] for i in range(0, len(button), 2)])