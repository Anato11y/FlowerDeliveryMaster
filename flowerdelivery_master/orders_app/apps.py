from django.apps import AppConfig


class OrdersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders_app'
    def ready(self):
       from . import signals # Импорт сигналов