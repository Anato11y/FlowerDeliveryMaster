import requests
from orders_app.models import Order, OrderItem

API_TOKEN = '7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo'
CHAT_ID = '551378516'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"

def notify_new_order(order_id: int):
    """
    Уведомление о новом заказе через синхронный Telegram API.
    """
    try:
        # Загружаем заказ из базы данных
        order = Order.objects.select_related('user').get(pk=order_id)

        # Формируем список товаров
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

        # Проверка: если сообщение пустое, не отправляем
        if not items_details.strip():
            return  # Прекращаем выполнение, если состав заказа пуст

        # Отправляем сообщение через Telegram API
        response = requests.post(
            TELEGRAM_API_URL,
            data={'chat_id': CHAT_ID, 'text': message},
            timeout=10
        )

        if response.status_code != 200:
            print(f"Ошибка при отправке сообщения: {response.text}")

    except Order.DoesNotExist:
        print(f"Заказ с ID {order_id} не найден.")
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения через Telegram: {e}")

def notify_order_status(order_id: int, status: str):
    """
    Уведомление об изменении статуса заказа через синхронный Telegram API.
    """
    message = f"Статус заказа #{order_id} изменён на: {status}"
    try:
        response = requests.post(
            TELEGRAM_API_URL,
            data={'chat_id': CHAT_ID, 'text': message},
            timeout=10
        )

        if response.status_code != 200:
            raise ValueError(f"Ошибка при отправке сообщения: {response.text}")

    except requests.RequestException:
        pass
