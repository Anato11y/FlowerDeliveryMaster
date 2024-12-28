from django.urls import path, include
from . import views

app_name = 'orders'

urlpatterns = [
    # Каталог и управление товарами в каталоге
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/update/<int:flower_id>/', views.update_catalog_item_in_catalog, name='update_catalog_item_in_catalog'),

    # Корзина и управление товарами в корзине
    path('cart/', views.cart, name='cart'),
    path('update/<int:flower_id>/', views.update_cart_item, name='update_cart_item'),

    # Оформление заказа и история заказов
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='history'),

    # Аутентификация
    path('accounts/', include('django.contrib.auth.urls')),  # Встроенные auth URL'ы
    path('accounts/register/', views.register, name='register'),
]
