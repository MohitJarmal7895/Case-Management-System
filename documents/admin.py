from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'case', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'case')
    search_fields = ('title', 'description', 'case__title')
    date_hierarchy = 'uploaded_at'
