from django.contrib import admin
from django.utils.html import format_html
from .models import Department, Staff, TimeLog

# Register your models here.
admin.site.register(Department)
admin.site.register(TimeLog)

# Register Staff with the custom StaffAdmin
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_username', 'first_name', 'last_name', 'position', 'department', 'photo_thumbnail')  # Columns to show
    search_fields = ('staff_username', 'first_name', 'last_name', 'position')  # Search bar fields
    list_filter = ('department', 'position')  # Filters on the right

    def photo_thumbnail(self, obj):
        # If the photo exists, display it as an HTML image tag
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
        return "No Photo"

    photo_thumbnail.short_description = 'Photo'  # This sets the column header for the photo