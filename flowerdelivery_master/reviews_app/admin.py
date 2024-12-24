from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'flower', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')