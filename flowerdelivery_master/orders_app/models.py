from django.db import models
from django.contrib.auth.models import User

class Flower(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)  # поле для описания
    image = models.ImageField(upload_to='flowers', blank=True, null=True)  # поле для картинки

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает обработки'),
        ('in_progress', 'В процессе'),
        ('delivered', 'Доставлено'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    customer_name = models.CharField(max_length=255)  # Добавляем поле имени клиента
    flowers = models.ManyToManyField('Flower', through='OrderItem')  # Продукты в заказе
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания заказа
    status = models.CharField(max_length=50, default='new')  # Статус заказа
    def __str__(self):
        return f"Заказ #{self.pk} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Связь с заказом
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)  # Связь с цветком
    quantity = models.PositiveIntegerField()  # Количество

    def __str__(self):
        return f"{self.quantity} x {self.flower.name} (Order #{self.order.id})"