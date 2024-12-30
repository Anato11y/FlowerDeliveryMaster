from django.shortcuts import render
from django.db.models import Sum, Count, Avg, F
from datetime import timedelta, datetime
from django.utils import timezone
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from orders_app.models import Order, OrderItem, Flower


def dashboard(request):
    # Определяем временной интервал
    one_month_ago = timezone.now() - timedelta(days=30)
    today = datetime.now().date()

    # Метрики
    total_sales = (
        OrderItem.objects.filter(order__status='delivered')
        .aggregate(total=Sum(F('quantity') * F('flower__price')))['total']
        or 0
    )

    total_orders = Order.objects.filter(status='delivered').count()

    average_order_result = (
        OrderItem.objects.filter(order__status='delivered')
        .values('order')
        .annotate(order_total=Sum(F('quantity') * F('flower__price')))
        .aggregate(avg=Avg('order_total'))['avg']
        or 0
    )
    average_order = round(average_order_result, 2)

    monthly_sales = (
        OrderItem.objects.filter(order__status='delivered', order__created_at__gte=one_month_ago)
        .aggregate(total=Sum(F('quantity') * F('flower__price')))['total']
        or 0
    )
    monthly_orders = Order.objects.filter(status='delivered', created_at__gte=one_month_ago).count()

    top_products = (
        OrderItem.objects.filter(order__status='delivered')
        .values('flower__name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:5]
    )

    # Новые клиенты за последний месяц
    new_customers = (
        Order.objects.filter(status='delivered', created_at__gte=one_month_ago)
        .values('user')
        .distinct()
        .count()
    )

    # Статистика по статусам за сегодня
    orders_today = Order.objects.filter(created_at__date=today)
    status_counts = orders_today.values('status').annotate(count=Count('id'))

    labels = [status['status'] for status in status_counts]
    sizes = [status['count'] for status in status_counts]

    # Построение круговой диаграммы
    if sizes:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.title('Статусы заказов за сегодня')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
    else:
        chart_base64 = None

    # Передача данных в шаблон
    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'average_order': average_order,
        'monthly_sales': monthly_sales,
        'monthly_orders': monthly_orders,
        'top_products': top_products,
        'new_customers': new_customers,
        'chart': chart_base64,
    }
    return render(request, 'analytics_app/dashboard.html', context)
