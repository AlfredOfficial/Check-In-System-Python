from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)  # Department name
    
    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    staff_username = models.CharField(max_length=100, unique=True)  # Unique staff username
    first_name = models.CharField(max_length=100)  # Staff first name
    last_name = models.CharField(max_length=100)  # Staff last name
    position = models.CharField(max_length=100)  # Staff position
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Foreign key to Department
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True)  # Staff photo

    def __str__(self):
        return f'{self.first_name or "Unknown"} {self.last_name or "Unknown"} ({self.position or "No Position"})' # adding the or unknown


class TimeLog(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)  # ADDING PROTECT STAFF
    date = models.DateField()  # Date of the log
    time_in = models.TimeField()  # Check-in time
    time_out = models.TimeField()  # Check-out time

    # Choice for attendance status
    STATUS_CHOICES = [
        ('on_time', 'On Time'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='on_time')  # Attendance status

    def __str__(self):
        return f'{self.staff or "Unknown Staff"} - {self.date} - {self.status}'
