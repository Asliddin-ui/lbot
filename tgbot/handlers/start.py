from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from tgbot.customhandler import CustomHandler
from tgbot.keyboards import lang_button, get_contact, region_button, get_role, category_button, yes_no_button
from tgbot.models import TelegramUser, CategoryModel, RoleModel, RegionModel
from django.utils.translation import gettext as _, activate

from tgbot.validators import PhoneValidator

STATE = 'state',
STATE_ADD_FULLNAME = 'full_name',
STATE_ADD_PHONE = 'phone',
STATE_ADD_COUNTRY = 'country'
STATE_ADD_ROLE = 'role'
STATE_ADD_JOB = 'job'


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


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    params = {
        'text': _('Xush kelibsiz {}. Botdan foydalanish uchun tilni tanlang: ').format(
            update.effective_user.first_name),
        'reply_markup': await lang_button()
    }

    params3 = {
        'text': _('Pastdagi menulardan birini tanlang')
    }

    if context.user_data.get(STATE, '') == '':
        if context.user_data['edit'] and not context.user_data['lang']:
            await update.effective_message.reply_text(**params)
            context.user_data[STATE] = STATE
        else:
            await update.effective_message.reply_text(**params3)
    else:
        await update.message.delete()


async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['user'] = {'language': context.match.group(1)}
    activate(context.match.group(1))
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
        context.user_data['user'].update({'fullname': msg})
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


async def set_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get(STATE, '')
    await update.effective_message.delete()
    user = context.user_data.get('user', {})
    query = update.callback_query
    if state == STATE_ADD_COUNTRY:
        cid = int(query.data)
        context.user_data['user'].update({'cid': cid})
        context.user_data[STATE] = STATE_ADD_ROLE
        await update.effective_message.reply_text(_('Foydalanuvchi turini tanlang'),
                                                  reply_markup=await get_role())
    elif state == STATE_ADD_ROLE:
        cid = int(query.data)
        context.user_data['user'].update({'role_id': cid})
        context.user_data['user']['job'] = []
        if cid == 1:
            context.user_data[STATE] = STATE_ADD_JOB
            await update.effective_message.reply_text(_('Xizmat faoliyati: '),
                                                      reply_markup=await category_button(context=context))
        else:
            context.user_data[STATE] = ''
            await hello(update, context)

    elif state == STATE_ADD_JOB:
        selected_job = query.data
        if selected_job == 'yes':
            await update.effective_message.reply_text(_('Xizmat faoliyati: '),
                                                      reply_markup=await category_button(context=context))

            return

        elif selected_job == 'no':
            role = await RoleModel.objects.aget(id=user['role_id'])
            country = await RegionModel.objects.aget(id=user['cid'])
            category = [await CategoryModel.objects.aget(id=job)for job in user['job']]
            print(category)
            obj, created = await TelegramUser.objects.aupdate_or_create(
                telegram_user_id=update.effective_user.id,
                defaults={
                    "fullname": user['fullname'],
                    "phone": user['phone'],
                    "language": user['language'],
                    "role": role,
                    'region': country,
                }
            )
            obj.category.set(category)
            context.user_data[STATE] = ''
            await hello(update, context)
        else:
            context.user_data['user']['job'].append(int(selected_job))
            await update.effective_message.reply_text(_('Yana ish turi qoshasizmi?'),
                                                      reply_markup=await yes_no_button())
            return


async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


handlers = [
    (CustomHandler(user_load), 0),
    CommandHandler('start', hello),
    CallbackQueryHandler(change_language, pattern="^(uz|ru|en)$"),
    MessageHandler(filters.TEXT | filters.CONTACT | filters.COMMAND, add_fullname),
    CallbackQueryHandler(set_country, pattern='^([0-9])+$'),
    CallbackQueryHandler(set_country, pattern='^(yes|no)$')
]