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
from telegram_bot_app.bot import API_TOKEN

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
    # Функция для получения невыполненных заказов
    @sync_to_async
    def get_pending_orders():
        return list(
            Order.objects.exclude(status='delivered')
            .select_related('user')
        )

    # Проверяем, есть ли невыполненные заказы
    @sync_to_async
    def has_pending_orders():
        return Order.objects.exclude(status='delivered').exists()

    # Проверяем наличие невыполненных заказов
    pending_exist = await has_pending_orders()
    if not pending_exist:
        await update.message.reply_text("Нет невыполненных заказов.")
        return

    # Получаем список невыполненных заказов
    pending = await get_pending_orders()

    # Формируем сообщение
    message = "Невыполненные заказы:\n"
    for order in pending:
        message += (
            f"Заказ #{order.id}\n"
            f"Клиент: {order.user.username if order.user else 'Гость'}\n"
            f"Адрес доставки: {order.delivery_address}\n"
            f"Статус: {order.get_status_display()}\n\n"
        )

    await update.message.reply_text(message)
def main():
    # Создаём объект Application с вашим токеном
    application = Application.builder().token(API_TOKEN).build()
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analytics", analytics))
    application.add_handler(CommandHandler("pending_orders", pending_orders))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
