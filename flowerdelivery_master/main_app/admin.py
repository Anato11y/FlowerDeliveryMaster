from django.contrib import admin
from .models import Profile
from .models import SiteSettings

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
from .models import SiteSettings
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    class SiteSettingsAdmin(admin.ModelAdmin):
        list_display = ('timezone',)
        list_editable = ('timezone',)



