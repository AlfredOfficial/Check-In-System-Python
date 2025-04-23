from django.contrib import admin
from .models import UserTimeLog

# Register your models here.
@admin.register(UserTimeLog)

class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time_in', 'time_out', 'status', 'total_hours')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'task_description')
    ordering = ('-date',)
    readonly_fields = ('total_hours',)