from django.core.management.base import BaseCommand
from telegram_bot_app.bot import setup_bot

class Command(BaseCommand):
    help = "Запуск Telegram-бота"

    def handle(self, *args, **kwargs):
        self.stdout.write("Запуск Telegram-бота...")
        application = setup_bot()
        application.run_polling()

