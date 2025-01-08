from django.contrib import admin
from .models import Equipment


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_name', 'status', 'last_calibration_date', 'next_calibration_date', 'assigned_to')
    list_filter = ('status',)
    search_fields = ('equipment_name',)