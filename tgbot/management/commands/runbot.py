from django.core.management import BaseCommand
from telegram.ext import ContextTypes

from tgbot.application import app


class Command(BaseCommand):
    def handle(self, *args, **options):
        app.run_polling()
