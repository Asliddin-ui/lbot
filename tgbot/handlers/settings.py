from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters


async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    await update.effective_message.reply_text(msg)


handlers = [
    MessageHandler(filters.TEXT, change_language)
]