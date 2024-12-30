from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SiteSettings
from django.conf import settings

@receiver(post_save, sender=SiteSettings)
def update_timezone(sender, instance, **kwargs):
    settings.TIME_ZONE = instance.timezone