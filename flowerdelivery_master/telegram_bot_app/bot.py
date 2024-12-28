# telegram_bot_app/bot.py
import logging
from telegram import Bot
from telegram.error import TelegramError
from orders_app.models import Order, Flower, OrderItem

API_TOKEN = '7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo'
bot = Bot(token=API_TOKEN)

def notify_new_order(order_id: int):
    """
    Получает число (ID заказа), загружает сам заказ из БД,
    формирует сообщение и отправляет в Телеграм.
    """
    chat_id = '551378516'  # Замените на ваш реальный chat_id
    try:
        # Загружаем заказ из базы
        order = Order.objects.get(pk=order_id)

        # Если хотите, можно собрать список букетов:
        # items = OrderItem.objects.filter(order=order).select_related('flower')
        # bouquet = ", ".join([f"{item.quantity}x {item.flower.name}" for item in items])

        message = (
            f"Новый заказ!\n"
            f"Клиент: {order.user.username}\n"        # или order.customer_name
            f"Адрес доставки: {order.delivery_address}\n"
            f"Статус: {order.get_status_display()}"
        )
        # Если нужно добавить информацию о цветах, раскомментируйте и добавьте в текст
        # message += f"\nСостав: {bouquet}"

        bot.send_message(chat_id=chat_id, text=message)
    except Order.DoesNotExist:
        logging.error(f"Заказ #{order_id} не найден в базе.")
    except TelegramError as e:
        logging.error(f"Ошибка при отправке сообщения в Телеграм: {e}")

def notify_order_status(order_id: int, status: str):
    """
    Обновление статуса заказа в Телеграм.
    По аналогии, здесь можно загрузить заказ или просто отправить 'номер + статус'.
    """
    chat_id = '551378516'
    message = f"Статус заказа #{order_id} изменён на: {status}"
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        logging.error(f"Ошибка при отправке сообщения об обновлении статуса: {e}")