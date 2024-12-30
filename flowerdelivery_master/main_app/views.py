from django.shortcuts import render
from orders_app.models import Flower
from django.http import JsonResponse
def index(request):
    products = Flower.objects.all()[:5]  # Получить первые 5 товаров
    return render(request, 'main_app/index.html', {'products': products})
