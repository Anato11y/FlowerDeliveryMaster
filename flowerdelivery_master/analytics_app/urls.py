from django.urls import path
from . import views

app_name = 'analytics_app'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]
