from django.contrib import admin
from .models import Sample

# Register your models here.
@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('sample_id', 'sample_name', 'status', 'collection_date', 'completion_date')
    list_filter = ('status', 'collection_date')
    search_fields = ('sample_id', 'sample_name')


