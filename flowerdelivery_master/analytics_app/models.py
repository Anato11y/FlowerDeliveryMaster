from django.db import models
from orders_app.models import Order

class Report(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    sales_data = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def total_amount(self):
        return self.sales_data - self.expenses

    def __str__(self):
        return f"Отчёт по заказу #{self.order.id}"



