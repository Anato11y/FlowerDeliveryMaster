import os
import django
import logging

# Настраиваем Django окружение, чтобы иметь доступ к моделям
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowerdelivery_master.settings')
django.setup()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from orders_app.models import Order

# Вставьте ваш токен бота
BOT_TOKEN = 'ВАШ_TELEGRAM_BOT_TOKEN'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в FlowerDelivery Bot!\n"
        "Доступные команды:\n"
        "/orders - посмотреть последние заказы\n"
    )

async def orders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders = Order.objects.all().order_by('-created_at')[:5]
    if not orders:
        text = "Нет заказов."
    else:
        text = "Последние заказы:\n"
        for o in orders:
            text += f"Заказ #{o.id} - Статус: {o.get_status_display()}\n"
    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("orders", orders_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
