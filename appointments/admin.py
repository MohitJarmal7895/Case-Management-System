from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'date_time', 'created_by')
    list_filter = ('date_time', 'client')
    search_fields = ('title', 'description', 'client__name')
    date_hierarchy = 'date_time'
