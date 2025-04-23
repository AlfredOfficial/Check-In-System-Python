from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
# Create your models here.
class UserTimeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField()
    time_out = models.TimeField(null=True, blank=True)
    task_description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ], default='Pending')

    def total_hours(self):
        if self.time_in and self.time_out:
            delta = datetime.combine(date.min, self.time_out) - datetime.combine(date.min, self.time_in)
            return round(delta.total_seconds() / 3600, 2)
        return 0.0