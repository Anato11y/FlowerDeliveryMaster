import logging
from telegram import Bot
from telegram.error import TelegramError

# Токен вашего бота, который вы получили от BotFather
API_TOKEN = '7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo'

# Инициализация бота
bot = Bot(token=API_TOKEN)


# Функция для отправки сообщений
def send_order_notification(order_info):
    """Функция отправляет уведомление в Telegram о новом заказе"""
    chat_id = 'your-chat-id'  # Ваш chat_id или ID канала, куда бот будет отправлять сообщения
    message = f"Новый заказ:\n{order_info['customer_name']}\nБукет: {order_info['bouquet_name']}\nАдрес доставки: {order_info['delivery_address']}"

    try:
        bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")


def send_status_update(order_id, status):
    """Функция отправляет обновление статуса заказа"""
    chat_id = 'your-chat-id'  # Ваш chat_id или ID канала
    message = f"Статус заказа {order_id} изменен на: {status}"

    try:
        bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
