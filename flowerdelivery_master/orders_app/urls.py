from django.urls import path, include
from . import views

app_name = 'orders'

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/update/<int:flower_id>/', views.update_catalog_item_in_catalog, name='update_catalog_item_in_catalog'),
    path('cart/', views.cart, name='cart'),
    path('update/<int:flower_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='history'),
    # Аутентификация
    path('accounts/', include('django.contrib.auth.urls')),  # Включаем встроенные auth URL'ы
    path('accounts/register/', views.register, name='register'),  # Добавим путь для регистрации
    # ВАЖНО: вот этот маршрут нужен, если вы используете
    # {% url 'orders:update_catalog_item_in_catalog' flower_id %}
    path('catalog/update/<int:flower_id>/',
         views.update_catalog_item_in_catalog,  # <-- вьюха
         name='update_catalog_item_in_catalog'), # <-- имя, совпадающее с шаблоном

    # Существующий для корзины
    path('update/<int:flower_id>/', views.update_cart_item, name='update_cart_item'),
    path('repeat/<int:order_id>/', views.repeat_order, name='repeat_order'),
]
