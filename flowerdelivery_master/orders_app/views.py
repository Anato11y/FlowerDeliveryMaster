from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from asgiref.sync import sync_to_async
from django.contrib import messages
from django.db.models import Count, Sum
from .models import Flower, Order
from asgiref.sync import sync_to_async

async def catalog(request):
    #   Асинхронное представление каталога.

    # Получение всех цветов из базы данных

    all_flowers = await sync_to_async(list)(Flower.objects.all())

    # Обработка корзины из сессии
    cart = request.session.get('cart', {})
    if isinstance(cart, list):  # Если корзина вдруг список, преобразуем её
        new_cart = {}
        for f_id in cart:
            f_id_str = str(f_id)
            new_cart[f_id_str] = new_cart.get(f_id_str, 0) + 1
        request.session['cart'] = new_cart
        cart = new_cart

    # Если POST-запрос — добавление товара в корзину
    if request.method == 'POST':
        flower_id = request.POST.get('flower_id')
        if flower_id:
            current_qty = cart.get(flower_id, 0)
            cart[flower_id] = current_qty + 1
            request.session['cart'] = cart
        return redirect('orders:catalog')

    # Формируем список цветов с количеством
    flowers_with_qty = [{'flower': f, 'qty': cart.get(str(f.id), 0)} for f in all_flowers]

    return render(request, 'orders_app/catalog.html', {
        'flowers': flowers_with_qty
    })


@login_required
def update_catalog_item_in_catalog(request, flower_id):
    """
    Обрабатывает POST-запрос на изменение количества товара в каталоге.
    """
    cart = request.session.get('cart', {})
    str_id = str(flower_id)

    # Если товара нет в корзине, добавить с количеством 0
    if str_id not in cart:
        cart[str_id] = 0

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'plus':
            cart[str_id] += 1
        elif action == 'minus':
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]

        # Сохраняем изменения в сессии
        request.session['cart'] = cart

    return redirect('orders:catalog')

@login_required
async def cart(request):
    """
    Асинхронное представление корзины.
    """
    cart_dict = request.session.get('cart', {})

    if isinstance(cart_dict, list):
        new_cart = {}
        for flower_id in cart_dict:
            flower_id_str = str(flower_id)
            new_cart[flower_id_str] = new_cart.get(flower_id_str, 0) + 1
        request.session['cart'] = new_cart
        cart_dict = new_cart

    items = []
    total_sum = 0

    for flower_id, qty in cart_dict.items():
        try:
            flower = await sync_to_async(Flower.objects.get)(id=flower_id)
            cost = flower.price * qty
            total_sum += cost
            items.append({'flower': flower, 'qty': qty, 'cost': cost})
        except Flower.DoesNotExist:
            pass

    return render(request, 'orders_app/cart.html', {
        'items': items,
        'total_sum': total_sum
    })

@login_required
async def update_cart_item(request, flower_id):
    """
    Обрабатывает изменение количества товара в корзине.
    """
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        flower_id_str = str(flower_id)

        # Если товара нет в корзине, просто возвращаемся
        if flower_id_str not in cart:
            return redirect('orders:cart')

        action = request.POST.get('action')
        if action == 'plus':
            cart[flower_id_str] += 1
        elif action == 'minus':
            cart[flower_id_str] -= 1
            if cart[flower_id_str] <= 0:
                del cart[flower_id_str]  # Удаляем товар из корзины, если его количество <= 0

        # Сохраняем обновления в сессии
        request.session['cart'] = cart

    return redirect('orders:cart')
@login_required
async def checkout(request):
    """
    Асинхронное оформление заказа.
    """
    if request.method == 'POST':
        cart_dict = request.session.get('cart', {})
        if cart_dict:
            order = await sync_to_async(Order.objects.create)(user=request.user)
            for f_id, qty in cart_dict.items():
                try:
                    flower = await sync_to_async(Flower.objects.get)(id=f_id)
                    order.flowers.add(flower)
                except Flower.DoesNotExist:
                    pass
            await sync_to_async(order.save)()
            request.session['cart'] = {}
            return redirect('orders:history')
    return redirect('orders:cart')


@login_required
async def order_history(request):
    """
    Асинхронное представление истории заказов.
    """
    orders = await sync_to_async(list)(Order.objects.filter(user=request.user))
    return render(request, 'orders_app/history.html', {'orders': orders})


def register(request):
    """
    Регистрация нового пользователя.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно. Добро пожаловать!')
            return redirect('orders:catalog')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте форму ниже.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


async def order_analytics(request):
    """
    Асинхронная аналитика заказов.
    """
    orders_by_status = await sync_to_async(list)(Order.objects.values('status').annotate(count=Count('id')))
    total_income = await sync_to_async(lambda: Order.objects.aggregate(total=Sum('total_amount')))()
    return render(request, 'orders/analytics.html', {
        'orders_by_status': orders_by_status,
        'total_income': total_income,
    })
