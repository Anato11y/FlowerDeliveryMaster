from django.apps import AppConfig
import logging

class OrdersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders_app'
    def ready(self):
        logging.info("OrdersAppConfig.ready() вызван")
        import orders_app.signals  # Подключаем сигналы