from django.db import models
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
    customer_name = models.CharField(max_length=255)
    flowers = models.ManyToManyField('Flower', through='OrderItem')  # Связь через промежуточную таблицу
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    bouquet_name = models.CharField(max_length=255, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)  # Адрес доставки
    def __str__(self):
        return f"Заказ #{self.pk} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Связь с заказом
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)  # Связь с цветком
    quantity = models.PositiveIntegerField()  # Количество цветов

    def __str__(self):
        return f"{self.quantity} x {self.flower.name} (Order #{self.order.pk})"
