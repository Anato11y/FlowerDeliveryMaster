from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Avg, F, Count
from django.utils import timezone
from datetime import timedelta

from orders_app.models import Order, OrderItem, Flower

# Проверка, является ли пользователь администратором
def is_admin(user):
    return user.is_superuser or user.is_staff

# Декоратор для ограничения доступа
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if is_admin(request.user):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Доступ к этой странице запрещён.")
            return redirect('login')  # Используйте имя вашего URL для входа
    return _wrapped_view

# Панель администратора с аналитикой
@admin_required
def dashboard(request):
    one_month_ago = timezone.now() - timedelta(days=30)

    # Общие продажи за всё время
    total_sales = OrderItem.objects.aggregate(
        total_revenue=Sum(F('flower__price') * F('quantity'))
    )['total_revenue'] or 0

    # Общее количество завершённых заказов
    total_orders = Order.objects.filter(status='delivered').count()

    # Средняя сумма заказа
    average_order = OrderItem.objects.values('order').annotate(
        order_total=Sum(F('flower__price') * F('quantity'))
    ).aggregate(avg=Avg('order_total'))['avg'] or 0

    # Продажи за последний месяц
    monthly_sales = OrderItem.objects.filter(order__created_at__gte=one_month_ago).aggregate(
        total_revenue=Sum(F('flower__price') * F('quantity'))
    )['total_revenue'] or 0

    monthly_orders = Order.objects.filter(status='delivered', created_at__gte=one_month_ago).count()

    # Топ 5 продаваемых товаров
    top_products = OrderItem.objects.values('flower__name').annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:5]

    # Продажи по категориям (если есть категории у цветов)
    sales_by_category = OrderItem.objects.values('flower__name').annotate(
        total_sales=Sum(F('flower__price') * F('quantity'))
    ).order_by('-total_sales')

    # Новые клиенты за последний месяц
    new_customers = Order.objects.filter(status='delivered', created_at__gte=one_month_ago).values('user').distinct().count()

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

    return render(request, 'analytics_app/dashboard.html', context)

