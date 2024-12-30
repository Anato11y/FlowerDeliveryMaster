from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

class Flower(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='flowers/', verbose_name="Изображение", blank=True, null=True)

    def __str__(self):
        return self.name
class SiteSettings(models.Model):
    time_zone = models.CharField(
        max_length=50,
        default="Europe/Moscow",
        verbose_name="Часовой пояс"
    )
    start_work_time = models.TimeField(
        default="09:00",
        verbose_name="Начало рабочего времени"
    )
    end_work_time = models.TimeField(
        default="18:00",
        verbose_name="Конец рабочего времени"
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"