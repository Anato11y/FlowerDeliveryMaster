from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order
from telegram_bot_app.bot import send_order_notification, send_status_update

@receiver(post_save, sender=Order)
def send_order_created_notification(sender, instance, created, **kwargs):
    """Отправка уведомления о новом заказе"""
    if created:
        order_info = {
            'customer_name': instance.customer_name,
            'bouquet_name': instance.bouquet_name,
            'delivery_address': instance.delivery_address
        }
        send_order_notification(order_info)

@receiver(pre_save, sender=Order)
def send_order_status_update(sender, instance, **kwargs):
    """Отправка уведомления об изменении статуса заказа"""
    if instance.pk:
        old_status = Order.objects.get(pk=instance.pk).status
        if old_status != instance.status:
            send_status_update(instance.id, instance.status)
