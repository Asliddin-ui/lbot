from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters

from tgbot.handlers import start, settings
from tgbot.keyboards import get_contact, region_button, get_role, category_button, yes_no_button
from tgbot.models import TelegramUser,  RoleModel, RegionModel
from django.utils.translation import gettext as _, activate

from tgbot.validators import PhoneValidator

STATE = 'state',
STATE_ADD_FULLNAME = 'full_name',
STATE_ADD_PHONE = 'phone',
STATE_ADD_COUNTRY = 'country'
STATE_ADD_ROLE = 'role'
STATE_ADD_JOB = 'job'


async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user: TelegramUser = context.user_data['tg_user']
    user.language = context.match.group(1)
    await user.asave()
    activate(user.language)
    await update.callback_query.answer(_('Til o`zgartirildi'))
    await update.effective_message.delete()
    await update.effective_message.reply_text('Ismingizni kiriting')
    context.user_data[STATE] = STATE_ADD_FULLNAME


async def add_fullname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    state = context.user_data.get(STATE, '')
    if state == STATE_ADD_FULLNAME:
        if msg.startswith('/'):
            await update.effective_message.reply_text('Iltimos ismni to`gri kiriting')
            return
        await update.effective_message.reply_text(
            'Telefon raqamingizni +998901234567 shaklida yuboring yoki pastdagi tugmani bosing',
            reply_markup=await get_contact())
        context.user_data['user'] = {'fullname': msg}
        context.user_data[STATE] = STATE_ADD_PHONE
    elif state == STATE_ADD_PHONE:
        contact = ''
        if msg:
            contact = msg
        elif update.message.contact:
            contact = update.message.contact.phone_number
        if PhoneValidator.validate(PhoneValidator.clean(contact)):
            try:
                await TelegramUser.objects.aget(phone=PhoneValidator.clean(contact))
                await update.effective_message.reply_text(
                    _('Bu raqam avval ro`yxatdan o`tgan iltimos boshqa raqam kiriting'),
                )
                return
            except TelegramUser.DoesNotExist:
                await update.effective_message.reply_text(_('Viloyat tanlang'), reply_markup=await region_button())
                context.user_data['user'].update({'phone': PhoneValidator.clean(contact)})
                context.user_data[STATE] = STATE_ADD_COUNTRY
        else:
            await update.effective_message.reply_text(_('Raqam noto`g`ri iltimos boshqa raqam kiriting'))
            return
    else:
        await settings.change_language(update, context)


async def set_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get(STATE, '')
    await update.effective_message.delete()
    query = update.callback_query
    if state == STATE_ADD_COUNTRY:
        region = await RegionModel.objects.aget(id=int(query.data))
        context.user_data['user'].update({'region': region})
        context.user_data[STATE] = STATE_ADD_ROLE
        await update.effective_message.reply_text(_('Foydalanuvchi turini tanlang'),
                                                  reply_markup=await get_role())
    elif state == STATE_ADD_ROLE:
        cid = int(query.data)
        role = await RoleModel.objects.aget(id=cid)
        context.user_data['user'].update({'role': role})
        if cid == 1:
            context.user_data[STATE] = STATE_ADD_JOB
            context.user_data['category'] = []
            await update.effective_message.reply_text(_('Xizmat faoliyati: '),
                                                      reply_markup=await category_button(context=context))
        else:
            print(context.user_data['user'])
            for key, value in context.user_data['user'].items():
                setattr(context.user_data['tg_user'], key, value)

            await context.user_data['tg_user'].asave()
            context.user_data[STATE] = ''
            await start.hello(update, context)

    elif state == STATE_ADD_JOB:
        selected_job = query.data
        if selected_job == 'yes':
            await update.effective_message.reply_text(_('Xizmat faoliyati: '),
                                                      reply_markup=await category_button(context=context))

            return

        elif selected_job == 'no':
            print(context.user_data['user'])
            for key, value in context.user_data['user'].items():
                setattr(context.user_data['tg_user'], key, value)
            await context.user_data['tg_user'].category.aset(context.user_data['category'])
            await context.user_data['tg_user'].asave()

            context.user_data[STATE] = ''
            await start.hello(update, context)
        else:
            context.user_data['category'].append(int(selected_job))
            await update.effective_message.reply_text(_('Yana ish turi qoshasizmi?'),
                                                      reply_markup=await yes_no_button())
            return


handlers = [
    CallbackQueryHandler(change_language, pattern="^(uz|ru|en)$"),
    MessageHandler(filters.TEXT | filters.CONTACT | filters.COMMAND, add_fullname),
    CallbackQueryHandler(set_country, pattern='^([0-9])+$'),
    CallbackQueryHandler(set_country, pattern='^(yes|no)$')
]
