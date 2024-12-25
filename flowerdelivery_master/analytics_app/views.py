from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Avg, F, Count  # Добавлен Count
from django.utils import timezone
from datetime import timedelta

# Импорты моделей
from .models import Report
from orders_app.models import Order, Flower  # Импортируем Flower, так как используется ManyToManyField

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

    # Общие продажи за все время
    total_sales = Order.objects.filter(status='delivered').annotate(
        total_amount=Sum(F('flowers__price'))
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Общее количество завершённых заказов
    total_orders = Order.objects.filter(status='delivered').count()

    # Средняя сумма заказа
    average_order = Order.objects.filter(status='delivered').annotate(
        total_amount=Sum(F('flowers__price'))
    ).aggregate(avg=Avg('total_amount'))['avg'] or 0

    # Продажи за последний месяц
    monthly_sales = Order.objects.filter(status='delivered', created_at__gte=one_month_ago).annotate(
        total_amount=Sum(F('flowers__price'))
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    monthly_orders = Order.objects.filter(status='delivered', created_at__gte=one_month_ago).count()

    # Топ 5 продаваемых товаров
    top_products = Order.objects.filter(status='delivered').values('flowers__name').annotate(
        total_quantity=Count('flowers')
    ).order_by('-total_quantity')[:5]

    # Продажи по категориям (если есть категории у цветов)
    sales_by_category = Flower.objects.values('name').annotate(
        total_sales=Sum('price')
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
