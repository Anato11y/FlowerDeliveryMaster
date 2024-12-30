from django.utils.timezone import localtime, now
from pytz import timezone
from .models import SiteSettings

def get_site_settings():
    try:
        return SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        return None

def check_working_hours():
    """Проверяет, находится ли текущее время в рабочем диапазоне."""
    settings = get_site_settings()
    if not settings:
        # Если настройки отсутствуют, используем значения по умолчанию
        start_time = "09:00"
        end_time = "18:00"
        tz = "Europe/Moscow"
    else:
        start_time = settings.start_work_time
        end_time = settings.end_work_time
        tz = settings.time_zone

    # Применяем часовой пояс
    current_time = localtime(now(), timezone(tz)).time()
    return start_time <= current_time <= end_time

def get_time_zone():
    try:
        settings = SiteSettings.objects.first()
        return settings.time_zone if settings else "Europe/Moscow"
    except SiteSettings.DoesNotExist:
        return "Europe/Moscow"