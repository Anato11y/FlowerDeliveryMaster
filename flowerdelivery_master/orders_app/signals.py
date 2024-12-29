# orders_app/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from orders_app.models import Order
from .models import Order
from telegram_bot_app.bot import notify_new_order, notify_order_status

@receiver(post_save, sender=Order)
def send_order_created_notification(sender, instance, created, **kwargs):
    """Отправка уведомления о новом заказе"""
    if created:
        order_info = {
            'customer_name': instance.user.username,
            'bouquet_name': ", ".join([flower.name for flower in instance.flowers.all()]),
            'delivery_address': instance.delivery_address
        }
        notify_new_order(instance.pk) # <-- передаём число

@receiver(pre_save, sender=Order)
def send_order_status_update(sender, instance, **kwargs):
    if instance.pk:
        old_status = Order.objects.get(pk=instance.pk).status
        if old_status != instance.status:
            notify_order_status(instance.id, instance.status)
