from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from telegram_bot_app.bot import notify_new_order, notify_order_status
from .models import Order

@receiver(post_save, sender=Order)
def send_order_notifications(sender, instance, created, **kwargs):
    """Отправляет уведомления о новом заказе или изменении статуса заказа."""
    if created:
        # Уведомление о новом заказе
        async_to_sync(notify_new_order)(instance.pk)
    else:
        # Уведомление об изменении статуса заказа
        async_to_sync(notify_order_status)(instance.pk)


