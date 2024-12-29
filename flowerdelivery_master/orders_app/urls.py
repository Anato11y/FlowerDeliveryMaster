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

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),

    # Повтор заказа
    path('repeat/<int:order_id>/', views.repeat_order, name='repeat_order'),
    path('update_cart_item/<int:flower_id>/', views.update_cart_item, name='update_cart_item'),
    path('delete_cart_item/<int:flower_id>/', views.delete_cart_item, name='delete_cart_item'),
]
