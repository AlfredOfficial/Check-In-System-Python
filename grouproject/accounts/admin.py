from django.contrib import admin
from .models import Department, Staff, TimeLog

# Register your models here.
admin.site.register(Department)
admin.site.register(TimeLog)

# Register Staff with the custom StaffAdmin
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_username', 'first_name', 'last_name', 'position', 'department')  # Columns to show
    search_fields = ('staff_username', 'first_name', 'last_name', 'position')  # Search bar fields
    list_filter = ('department', 'position')  # Filters on the right