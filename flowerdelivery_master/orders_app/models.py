from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram import Bot
from django.contrib.auth.models import User


class Flower(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='flowers', blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает обработки'),
        ('in_progress', 'В процессе'),
        ('delivered', 'Доставлено'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"Заказ #{self.pk} от {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.flower.name}"


# Уведомление о новом заказе
@receiver(post_save, sender=Order)
def send_new_order_notification(sender, instance, created, **kwargs):
    bot = Bot("7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo")
    chat_id = "551378516"

    if created:
        # Формируем информацию о товарах
        items = OrderItem.objects.filter(order=instance)
        items_info = "\n".join([f"{item.quantity}x {item.flower.name}" for item in items])

        # Сообщение
        message = (
            f"Новый заказ!\n"
            f"Заказ №: {instance.pk}\n"
            f"Клиент: {instance.user.username}\n"
            f"Адрес доставки: {instance.delivery_address}\n"
            f"Статус: {instance.get_status_display()}\n\n"
            f"Состав заказа:\n{items_info}"
        )
        bot.send_message(chat_id=chat_id, text=message)

# Уведомление о статусе заказа
@receiver(post_save, sender=Order)
def send_order_status_notification(sender, instance, created, **kwargs):
    if not created:  # Если заказ уже существует и статус изменён
        bot = Bot("7851649387:AAE0ovMqW7U3WFL6pCetd3aQLMwoJptuKwo")
        chat_id = "551378516"

        message = (
            f"Статус заказа №{instance.pk} обновлён:\n"
            f"Текущий статус: {instance.get_status_display()}"
        )
        bot.send_message(chat_id=chat_id, text=message)
