from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum, F
from .models import Flower, Order, OrderItem
from telegram_bot_app.bot import notify_new_order, notify_order_status
from asgiref.sync import sync_to_async, async_to_sync


def catalog(request):
    """Каталог цветов с добавлением в корзину."""
    all_flowers = Flower.objects.all()
    cart = request.session.get('cart', {})

    if not cart:
        cart = {}
        request.session['cart'] = cart

    if request.method == 'POST':
        flower_id = request.POST.get('flower_id')
        if flower_id:
            cart[flower_id] = cart.get(flower_id, 0) + 1
            request.session['cart'] = cart
        return redirect('orders:catalog')

    flowers_with_qty = [
        {'flower': f, 'qty': cart.get(str(f.id), 0)} for f in all_flowers
    ]

    return render(request, 'orders_app/catalog.html', {'flowers': flowers_with_qty})


@login_required
def update_catalog_item_in_catalog(request, flower_id):
    """Изменение количества товара прямо в каталоге."""
    cart = request.session.get('cart', {})
    str_id = str(flower_id)

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
        request.session['cart'] = cart

    return redirect('orders:catalog')


@login_required
def cart(request):
    """Асинхронное представление корзины."""
    cart_dict = request.session.get('cart', {})
    items = []
    total_sum = 0

    for flower_id, qty in cart_dict.items():
        try:
            flower =Flower.objects.get(id=flower_id)
            cost = flower.price * qty
            total_sum += cost
            items.append({'flower': flower, 'qty': qty, 'cost': cost})
        except Flower.DoesNotExist:
            messages.error(request, f"Товар с ID {flower_id} был удалён.")

    return render(request, 'orders_app/cart.html', {'items': items, 'total_sum': total_sum})


@login_required
async def update_cart_item(request, flower_id):
    """Изменение количества товара в корзине."""
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        # Проверяем, есть ли товар в корзине
        if str(flower_id) not in cart:
            return redirect('orders:cart')

        action = request.POST.get('action')

        # Обрабатываем действия
        if action == 'plus':
            cart[str(flower_id)] += 1
        elif action == 'minus':
            cart[str(flower_id)] -= 1
            if cart[str(flower_id)] <= 0:
                del cart[str(flower_id)]
        elif action == 'delete':
            del cart[str(flower_id)]  # Удаление товара из корзины

        # Сохраняем обновлённую корзину в сессии
        request.session['cart'] = cart

    return redirect('orders:cart')


@login_required
async def checkout(request):
    """Оформление заказа (асинхронное)."""
    if request.method == 'POST':
        # Обёртка обращения к сессии
        cart = await sync_to_async(lambda: request.session.get('cart', {}))()
        # Обёртка обращения к POST-данным
        delivery_address = await sync_to_async(lambda: request.POST.get('delivery_address', ''))()

        # Создание заказа через ORM
        order = await sync_to_async(Order.objects.create)(
            user=request.user,
            delivery_address=delivery_address
        )

        # Добавление товаров в заказ
        for f_id, quantity in cart.items():
            flower = await sync_to_async(Flower.objects.get)(id=f_id)
            await sync_to_async(OrderItem.objects.create)(
                order=order,
                flower=flower,
                quantity=quantity
            )

        # Очистка корзины (сессии)
        await sync_to_async(lambda: request.session.update({'cart': {}}))()

        # Сообщение об успехе (messages — синхронный)
        await sync_to_async(messages.success)(
            request,
            f"Ваш заказ №{order.pk} успешно оформлен!"
        )

        # Вызов уведомления (если notify_new_order — синхронная)
        await sync_to_async(notify_new_order)(order.pk)

        # Перенаправление
        return redirect('orders:history')
    return redirect('orders:cart')

@login_required
def order_history(request):
    """История заказов."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items__flower').annotate(
        total_cost=Sum(F('items__quantity') * F('items__flower__price'))
    )
    return render(request, 'orders_app/history.html', {'orders': orders})


@login_required
def repeat_order(request, order_id):
    """Повторение заказа."""
    original_order = get_object_or_404(Order, pk=order_id, user=request.user)
    new_order = Order.objects.create(
        user=request.user,
        delivery_address=original_order.delivery_address
    )

    for item in original_order.items.all():
        OrderItem.objects.create(order=new_order, flower=item.flower, quantity=item.quantity)

    messages.success(request, f"Ваш заказ №{new_order.pk} успешно повторён!")
    return redirect('orders:history')


def register(request):
    """Регистрация нового пользователя."""
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
def delete_cart_item(request, flower_id):
    """Удаление товара из корзины."""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if str(flower_id) in cart:
            del cart[str(flower_id)]  # Удаляем товар из корзины
            request.session['cart'] = cart  # Обновляем сессию
    return redirect('orders:cart')  # Перенаправляем на страницу корзины