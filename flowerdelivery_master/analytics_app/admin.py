from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('order', 'date', 'sales_data', 'profit', 'expenses')

