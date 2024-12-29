from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from orders_app.models import Order
from telegram_bot_app.bot import notify_new_order, notify_order_status

@receiver(post_save, sender=Order)
def send_order_created_notification(sender, instance, created, **kwargs):
    """Уведомление о новом заказе"""
    if created:  # Срабатывает только при создании нового заказа
        try:
            # Отправляем уведомление о новом заказе
            notify_new_order(instance.pk)
        except Exception:
            pass

@receiver(pre_save, sender=Order)
def send_order_status_update(sender, instance, **kwargs):
    """Обновление статуса заказа"""
    if instance.pk:  # Если заказ уже существует
        try:
            old_status = Order.objects.get(pk=instance.pk).status
            if old_status != instance.status:
                # Отправляем уведомление об изменении статуса
                notify_order_status(instance.id, instance.status)
        except Order.DoesNotExist:
            pass
        except Exception:
            pass
