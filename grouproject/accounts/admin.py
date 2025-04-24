from django.contrib import admin
from .models import Department, Staff, TimeLog

# Register your models here.
admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(TimeLog)