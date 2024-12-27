from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from asgiref.sync import sync_to_async
from flowerdelivery_master.orders_app.models import Order, OrderItem
from orders_app.models import Order, OrderItem

TOKEN = "7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo"
CHAT_ID = "551378516"  # Укажите ваш Telegram chat_id

# Уведомление о новом заказе
async def notify_new_order(order_id):
    """Уведомление о новом заказе"""
    bot = Bot(TOKEN)
    order = await sync_to_async(Order.objects.get)(pk=order_id)

    items = await sync_to_async(list)(order.items.all())
    items_info = "\n".join([f"{item.quantity}x {item.flower.name}" for item in items])

    message = (
        f"Новый заказ!\n"
        f"Заказ №{order.pk}\n"
        f"Клиент: {order.user.username}\n"
        f"Адрес доставки: {order.delivery_address}\n"
        f"Статус: {order.get_status_display()}\n\n"
        f"Состав заказа:\n{items_info}"
    )
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Уведомление об изменении статуса заказа
async def notify_order_status(order_id):
    """Уведомление об изменении статуса заказа"""
    bot = Bot(TOKEN)
    order = await sync_to_async(Order.objects.get)(pk=order_id)

    message = (
        f"Статус заказа №{order.pk} обновлён:\n"
        f"Текущий статус: {order.get_status_display()}"
    )
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственная команда"""
    await update.message.reply_text("Добро пожаловать! Я бот для уведомлений о заказах и аналитики.")

# Команда /analytics (пример)
async def analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пример команды аналитики"""
    total_orders = await sync_to_async(Order.objects.count)()
    message = f"Аналитика заказов:\nВсего заказов: {total_orders}"
    await update.message.reply_text(message)

# Настройка бота
def setup_bot():
    """Настраивает и возвращает объект Application"""
    application = Application.builder().token(TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("analytics", analytics))

    return application
