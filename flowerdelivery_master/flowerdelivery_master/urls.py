from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('orders/', include('orders_app.urls')),
    path('reviews/', include('reviews_app.urls')),
    path('analytics/', include('analytics_app.urls', namespace='analytics')),
    path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
