from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Flower, Order
from django.contrib import messages
from django.db.models import Count, Sum
def catalog(request):
    """
    Каталог.
    1) Отображаем список всех Flower (flowers).
    2) Для POST-запроса ("добавить товар на +1") — если передаётся 'flower_id' без кнопок +/-.
    3) Если хотим использовать +/- (update в каталоге), используем отдельную вьюху update_catalog_item_in_catalog.
    """

    # 1. Загружаем все цветы
    all_flowers = Flower.objects.all()

    # 2. Забираем корзину из сессии
    cart = request.session.get('cart', {})

    # -- Проверка: если cart всё ещё список, конвертируем --
    if isinstance(cart, list):
        new_cart = {}
        for f_id in cart:
            f_id_str = str(f_id)
            new_cart[f_id_str] = new_cart.get(f_id_str, 0) + 1
        request.session['cart'] = new_cart
        cart = new_cart

    # 3. Если POST-запрос с flower_id (добавление на +1)
    #    (классический вариант «Добавить в корзину» одной кнопкой)
    if request.method == 'POST':
        flower_id = request.POST.get('flower_id')
        if flower_id:
            current_qty = cart.get(flower_id, 0)
            cart[flower_id] = current_qty + 1
            request.session['cart'] = cart
        return redirect('orders:catalog')  # обновить страницу

    # 4. Формируем список, где у каждого Flower есть поле "qty" (сколько уже лежит в корзине)
    flowers_with_qty = []
    for f in all_flowers:
        qty_in_cart = cart.get(str(f.id), 0)
        flowers_with_qty.append({
            'flower': f,
            'qty': qty_in_cart
        })

    return render(request, 'orders_app/catalog.html', {
        'flowers': flowers_with_qty
    })


@login_required
def update_catalog_item_in_catalog(request, flower_id):
    """
    Обрабатывает POST-запрос на +/- количество товара, когда пользователь нажимает «+»/«-» в КАТАЛОГЕ.
    Затем редиректит обратно на страницу каталога.
    """
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        str_id = str(flower_id)

        # Если товара нет в корзине — начинаем с 0
        if str_id not in cart:
            cart[str_id] = 0

        action = request.POST.get('action')
        if action == 'plus':
            cart[str_id] += 1
        elif action == 'minus':
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]

        # Сохраняем новые данные
        request.session['cart'] = cart

    return redirect('orders:catalog')


@login_required
def cart(request):
    """
    Страница корзины. Собираем словарь cart из сессии,
    вытягиваем соответствующие объекты Flower и их количество.
    """
    cart_dict = request.session.get('cart', {})

    # Если cart_dict оказался СПИСКОМ, конвертируем в СЛОВАРЬ
    if isinstance(cart_dict, list):
        new_cart = {}
        for flower_id in cart_dict:
            flower_id_str = str(flower_id)
            new_cart[flower_id_str] = new_cart.get(flower_id_str, 0) + 1
        request.session['cart'] = new_cart
        cart_dict = new_cart

    items = []
    total_sum = 0

    # cart_dict теперь { '1': 2, '2': 1 } и т.д.
    for flower_id, qty in cart_dict.items():
        try:
            flower = Flower.objects.get(id=flower_id)
            cost = flower.price * qty
            total_sum += cost
            items.append({
                'flower': flower,
                'qty': qty,
                'cost': cost
            })
        except Flower.DoesNotExist:
            pass  # Если товар был удалён из базы

    return render(request, 'orders_app/cart.html', {
        'items': items,
        'total_sum': total_sum
    })


@login_required
def update_cart_item(request, flower_id):
    """
    Обрабатывает POST-запрос на +/- количество товара (в корзине).
    Параметр flower_id приходит через URL: /orders/update/<flower_id>/
    В форме используем name="action" со значениями "plus" или "minus".
    """
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        str_id = str(flower_id)

        # Если вдруг товара нет в корзине, просто редирект
        if str_id not in cart:
            return redirect('orders:cart')

        action = request.POST.get('action')
        if action == 'plus':
            cart[str_id] += 1
        elif action == 'minus':
            cart[str_id] -= 1
            if cart[str_id] <= 0:
                del cart[str_id]  # убрать товар, если количество стало 0

        request.session['cart'] = cart

    return redirect('orders:cart')


@login_required
def checkout(request):
    """
    Оформление заказа.
    Проходим по cart, создаём Order, добавляем каждый цветок нужное кол-во раз.
    Очищаем корзину по завершении.
    """
    if request.method == 'POST':
        cart_dict = request.session.get('cart', {})
        if cart_dict:
            order = Order.objects.create(user=request.user)
            for f_id, qty in cart_dict.items():
                try:
                    flower = Flower.objects.get(id=f_id)
                    # Добавляем цветок qty раз
                    for _ in range(qty):
                        order.flowers.add(flower)
                except Flower.DoesNotExist:
                    pass
            order.save()
            # Очистка корзины
            request.session['cart'] = {}
            return redirect('orders:history')

    return redirect('orders:cart')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders_app/history.html', {'orders': orders})


def register(request):
    """
    Представление для регистрации нового пользователя.
    Использует встроенную форму UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически авторизуем пользователя после регистрации
            messages.success(request, 'Регистрация прошла успешно. Добро пожаловать!')
            return redirect('orders:catalog')  # Перенаправляем на каталог после успешной регистрации
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте форму ниже.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def order_analytics(request):
    # Получаем количество заказов по статусам
    orders_by_status = Order.objects.values('status').annotate(count=Count('id'))

    # Получаем сумму по заказам (например, для подсчета дохода)
    total_income = Order.objects.aggregate(total=Sum('total_amount'))  # Предположим, что у нас есть поле total_amount

    return render(request, 'orders/analytics.html', {
        'orders_by_status': orders_by_status,
        'total_income': total_income,
    })