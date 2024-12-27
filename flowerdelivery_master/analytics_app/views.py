from asgiref.sync import sync_to_async
from django.shortcuts import render
from django.db.models import Sum, Count, Avg, F
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import FieldError

from orders_app.models import Order, OrderItem, Flower

# Асинхронная панель администратора с аналитикой
async def dashboard(request):
    # Определяем временной интервал
    one_month_ago = timezone.now() - timedelta(days=30)

    # Общие продажи за все время
    total_sales_result = await sync_to_async(
        lambda: OrderItem.objects.filter(order__status='delivered').aggregate(
            total=Sum(F('quantity') * F('flower__price'))
        )
    )()
    total_sales = total_sales_result['total'] or 0

    # Общее количество завершённых заказов
    total_orders = await sync_to_async(
        lambda: Order.objects.filter(status='delivered').count()
    )()

    # Средняя сумма заказа
    average_order_result = await sync_to_async(
        lambda: OrderItem.objects.filter(order__status='delivered').values('order').annotate(
            order_total=Sum(F('quantity') * F('flower__price'))
        ).aggregate(avg=Avg('order_total'))
    )()
    average_order = average_order_result['avg'] or 0

    # Продажи за последний месяц
    monthly_sales_result = await sync_to_async(
        lambda: OrderItem.objects.filter(order__status='delivered', order__created_at__gte=one_month_ago).aggregate(
            total=Sum(F('quantity') * F('flower__price'))
        )
    )()
    monthly_sales = monthly_sales_result['total'] or 0
    monthly_orders = await sync_to_async(
        lambda: Order.objects.filter(status='delivered', created_at__gte=one_month_ago).count()
    )()

    # Топ 5 продаваемых товаров
    top_products = await sync_to_async(
        lambda: list(OrderItem.objects.filter(order__status='delivered').values(
            'flower__name'
        ).annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:5])
    )()

    # Продажи по категориям (если есть категории)
    try:
        sales_by_category = await sync_to_async(
            lambda: list(Flower.objects.values('category__name').annotate(
                total_sales=Sum(F('orderitem__quantity') * F('price'))
            ).order_by('-total_sales'))
        )()
    except FieldError:
        sales_by_category = []  # Если категорий нет, возвращаем пустой список

    # Новые клиенты за последний месяц
    new_customers = await sync_to_async(
        lambda: Order.objects.filter(status='delivered', created_at__gte=one_month_ago).values('user').distinct().count()
    )()

    # Подготовка данных для шаблона
    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'average_order': round(average_order, 2),
        'monthly_sales': monthly_sales,
        'monthly_orders': monthly_orders,
        'top_products': top_products,
        'sales_by_category': sales_by_category,
        'new_customers': new_customers,
    }

    # Рендеринг шаблона
    return await sync_to_async(render)(request, 'analytics_app/dashboard.html', context)
