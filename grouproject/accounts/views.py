from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Department, Staff, TimeLog


class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_superuser or user.is_staff:
                return redirect('/admin/')  # Redirect to admin dashboard
            elif hasattr(user, 'staff'):
                return redirect('/staff_dashboard/')  # Redirect to staff dashboard
            else:
                return redirect('/home/')
        return render(request, 'registration/login.html', {'form': form})


@login_required
def staff_dashboard(request):
    # Get the logged-in user's staff object
    
    staff_member = Staff.objects.get(user=request.user)
   

    # Fetch the TimeLog records for the logged-in staff
    time_logs = TimeLog.objects.filter(staff=staff_member).order_by('-date') if staff_member else []
    today = timezone.now().date()
    has_logged_in = time_logs.filter(date=today, time_in__isnull=False).exists()
    has_logged_out = time_logs.filter(date=today, time_out__isnull=False).exists()

    # Pass the staff data and time logs to the template
    return render(request, 'registration/staff_dashboard.html', {
        'staff_member': staff_member,
        'time_logs': time_logs,
        'has_logged_in': has_logged_in,
        'has_logged_out': has_logged_out
    })


@login_required
def time_in(request):
    # Log time in for the logged-in user
    staff_member = Staff.objects.get(user=request.user)
    TimeLog.objects.create(
        staff=staff_member,
        date=timezone.now().date(),
        time_in=timezone.now().time(),
        status='on_time'  # Default status when checking in
    )
    return redirect('staff_dashboard')  # Redirect to the staff dashboard


@login_required
def time_out(request):
    # Log time out for the logged-in user
    staff_member = Staff.objects.get(user=request.user)
    time_log = TimeLog.objects.filter(staff=staff_member, date=timezone.now().date(), time_out__isnull=True).first()

    if time_log:
        time_log.time_out = timezone.now().time()
        time_log.status = 'OUT'
        time_log.save()

    return redirect('staff_dashboard')  # Redirect to the staff dashboard
