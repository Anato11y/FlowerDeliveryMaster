# telegram_bot_app/bot.py
import logging
from telegram import Bot
from telegram.error import TelegramError

API_TOKEN = '7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo'
bot = Bot(token=API_TOKEN)

def notify_new_order(order_info: dict):
    chat_id = '551378516'
    message = (
        f"Новый заказ!\n"
        f"Клиент: {order_info.get('customer_name')}\n"
        f"Букет: {order_info.get('bouquet_name')}\n"
        f"Адрес: {order_info.get('delivery_address')}"
    )
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")

def notify_order_status(order_id: int, status: str):
    chat_id = '551378516'
    message = f"Статус заказа #{order_id} изменён на: {status}"
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        logging.error(f"Ошибка при обновлении статуса: {e}")
