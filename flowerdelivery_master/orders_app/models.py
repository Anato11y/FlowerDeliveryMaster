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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flowers = models.ManyToManyField(Flower)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.pk} от {self.user.username}"
