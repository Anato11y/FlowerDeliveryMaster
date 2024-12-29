import logging
from telegram import Bot
from telegram.error import TelegramError
from orders_app.models import Order, OrderItem
from asgiref.sync import async_to_sync
from telegram.request import HTTPXRequest

API_TOKEN = '7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo'
# Увеличиваем пул соединений
request = HTTPXRequest(read_timeout=10)
bot = Bot(token=API_TOKEN, request=request)

def notify_new_order(order_id: int):
    """
    Уведомление о новом заказе.
    """
    chat_id = '551378516'  # Замените на ваш реальный chat_id
    try:
        # Загружаем заказ из базы данных
        order = Order.objects.select_related('user').get(pk=order_id)

        # Проверяем, есть ли заказ
        if not order:
            logging.error(f"Заказ с ID {order_id} не найден.")
            return

        # Получаем список товаров в заказе
        order_items = OrderItem.objects.filter(order=order).select_related('flower')
        items_details = "\n".join(
            [f"{item.flower.name} x {item.quantity} шт. - {item.flower.price} руб./шт."
             for item in order_items]
        )

        # Формируем сообщение
        message = (
            f"Новый заказ #{order.id} создан!\n"
            f"Клиент: {order.user.username if order.user else 'Гость'}\n"
            f"Адрес доставки: {order.delivery_address}\n"
            f"Состав заказа:\n{items_details}\n"
            f"Общая стоимость: {sum(item.flower.price * item.quantity for item in order_items)} руб.\n"
            f"Статус: {order.get_status_display()}"
        )

        # Отправляем сообщение в Telegram
        async_to_sync(bot.send_message)(chat_id=chat_id, text=message)

    except Order.DoesNotExist:
        logging.error(f"Заказ с ID {order_id} не найден.")
    except TelegramError as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")


def notify_order_status(order_id: int, status: str):
    """
    Уведомление об изменении статуса заказа.
    """
    chat_id = '551378516'
    message = f"Статус заказа #{order_id} изменён на: {status}"
    try:
        async_to_sync(bot.send_message)(chat_id=chat_id, text=message)
    except TelegramError as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
