from .models import Report
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Count, Avg, F
from django.utils import timezone
from datetime import timedelta
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    reports = Report.objects.all().order_by('-date')
    return render(request, 'analytics_app/dashboard.html', {'reports': reports})

def is_admin(user):
    return user.is_superuser or user.is_staff

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if is_admin(request.user):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Доступ к этой странице запрещён.")
            return redirect('login')  # Используйте имя вашего URL для входа
    return _wrapped_view

@admin_required
def dashboard(request):
    # Ваша логика для аналитики

    # Общие продажи за все время
    total_sales = Order.objects.filter(status='completed').aggregate(total=Sum('total_amount'))['total'] or 0

    # Общее количество завершённых заказов
    total_orders = Order.objects.filter(status='completed').count()

    # Средняя сумма заказа
    average_order = Order.objects.filter(status='completed').aggregate(avg=Avg('total_amount'))['avg'] or 0

    # Продажи за последний месяц
    one_month_ago = timezone.now() - timedelta(days=30)
    monthly_sales = Order.objects.filter(status='completed', created_at__gte=one_month_ago).aggregate(total=Sum('total_amount'))['total'] or 0
    monthly_orders = Order.objects.filter(status='completed', created_at__gte=one_month_ago).count()

    # Топ 5 продаваемых товаров
    top_products = OrderItem.objects.filter(order__status='completed').values('product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

    # Продажи по категориям
    sales_by_category = OrderItem.objects.filter(order__status='completed').annotate(
        sales=F('price') * F('quantity')
    ).values('product__category').annotate(
        total_sales=Sum('sales')
    ).order_by('-total_sales')

    # Новые клиенты за последний месяц
    new_customers = Order.objects.filter(status='completed', created_at__gte=one_month_ago).values('customer').distinct().count()

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

