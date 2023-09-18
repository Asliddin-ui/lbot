from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from tgbot.customhandler import CustomHandler
from tgbot.handlers.registration import STATE
from tgbot.keyboards import lang_button, get_menu
from tgbot.models import TelegramUser
from django.utils.translation import gettext as _, activate


async def user_load(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user, _ = await TelegramUser.objects.aget_or_create(defaults={
        "username": update.effective_user.username,
        "fullname": update.effective_user.first_name,
        "language": update.effective_user.language_code,
        'phone': update.effective_user.id
    }, telegram_user_id=update.effective_user.id)

    context.user_data['edit'] = _
    context.user_data['tg_user'] = tg_user
    activate(tg_user.language)
    context.user_data['lang'] = False


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    params = {
        'text': _('Xush kelibsiz {}. Botdan foydalanish uchun tilni tanlang: ').format(
            update.effective_user.first_name),
        'reply_markup': await lang_button()
    }

    params3 = {
        'text': _('Pastdagi menulardan birini tanlang'),
        'reply_markup': await get_menu()

    }

    if context.user_data.get(STATE, '') == '':
        if context.user_data['edit'] and not context.user_data['lang']:
            await update.effective_message.reply_text(**params)
            context.user_data[STATE] = STATE
        else:
            await update.effective_message.reply_text(**params3)
    else:
        await update.message.delete()


handlers = [
    (CustomHandler(user_load), 0),
    CommandHandler('start', hello),
]
