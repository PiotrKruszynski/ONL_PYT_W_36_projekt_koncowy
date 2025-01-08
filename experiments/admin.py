from django.contrib import admin
from .models import Test, ResearchStandard


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'standard', 'status', 'start_date', 'end_date', 'technician', 'lab_member')
    list_filter = ('status', 'start_date')
    search_fields = ('test_name',)

@admin.register(ResearchStandard)
class ResearchStandardAdmin(admin.ModelAdmin):
    list_display = ('reaserch_st_name', 'method')
    search_fields = ('reaserch_st_name', 'method')
