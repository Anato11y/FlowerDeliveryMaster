import os
import django

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowerdelivery_master.settings')

# Инициализируем Django
django.setup()

from orders_app.models import Order  # Импорт модели после настройки Django
from django.db.models import Sum, Count, F
from telegram.ext import Application, CommandHandler
import datetime
from asgiref.sync import sync_to_async

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowerdelivery_master.settings')

# Инициализируем Django
django.setup()

# Функция обработчика для команды /start
async def start(update, context):
    await update.message.reply_text(
        "Бот запущен! Доступные команды:\n"
        "/help - помощь\n"
        "/analytics - аналитика за день\n"
        "/pending_orders - невыполненные заказы"
    )

# Функция обработчика для команды /help
async def help_command(update, context):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/help - помощь\n"
        "/analytics - аналитика за день\n"
        "/pending_orders - невыполненные заказы"
    )

# Функция обработчика для команды /analytics
async def analytics(update, context):
    # Получаем сегодняшнюю дату
    today = datetime.date.today()

    # Запрос аналитики для сегодняшних заказов
    @sync_to_async
    def get_analytics_data():
        return list(
            Order.objects.filter(created_at__date=today)
            .values('status')
            .annotate(
                total_orders=Count('id'),
                total_sum=Sum(F('items__quantity') * F('items__flower__price'))
            )
        )

    # Проверяем, есть ли заказы
    @sync_to_async
    def get_today_orders_count():
        return Order.objects.filter(created_at__date=today).exists()

    # Получаем данные
    orders_exist = await get_today_orders_count()
    if not orders_exist:
        await update.message.reply_text("Сегодня заказов не было.")
        return

    analytics_data = await get_analytics_data()

    # Формируем сообщение
    message = "Аналитика за сегодня:\n"
    for data in analytics_data:
        message += (
            f"Статус: {data['status']}\n"
            f"Количество заказов: {data['total_orders']}\n"
            f"Сумма: {data['total_sum'] or 0} руб.\n\n"
        )

    await update.message.reply_text(message)
# Функция обработчика для команды /pending_orders
async def pending_orders(update, context):
    # Реализация для невыполненных заказов
    await update.message.reply_text("Здесь будет информация о невыполненных заказах.")

def main():
    # Создаём объект Application с вашим токеном
    application = Application.builder().token("7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo").build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analytics", analytics))
    application.add_handler(CommandHandler("pending_orders", pending_orders))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
