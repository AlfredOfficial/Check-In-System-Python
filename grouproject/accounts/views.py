from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Staff, TimeLog


class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'accounts/registration/login.html', {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')  # Redirect to admin dashboard
            elif user.is_staff:
                return redirect('accounts/registration/staff_dashboard.html')  # Redirect to staff dashboard
            else:
                return redirect('home')
        return render(request, 'accounts/registration/login.html', {'form': form})


@login_required
def staff_dashboard(request):
    staff_member = Staff.objects.get(user=request.user)
    time_logs = TimeLog.objects.filter(staff=staff_member).order_by('-date')
    today = timezone.now().date()
    has_logged_in = time_logs.filter(date=today, time_in__isnull=False).exists()
    has_logged_out = time_logs.filter(date=today, time_out__isnull=False).exists()

    return render(request, 'accounts/registration/staff_dashboard.html', {
        'time_logs': time_logs,
        'has_logged_in': has_logged_in,
        'has_logged_out': has_logged_out
    })


@login_required
def time_in(request):
    # Log time in for the logged-in user
    staff_member = Staff.objects.get(user=request.user)
    time_log = TimeLog.objects.create(
        staff=staff_member,
        date=timezone.now().date(),
        time_in=timezone.now().time(),
        status='on_time'  # Default status when checking in
    )
    return redirect('accounts/registration/staff_dashboard.html')  # Redirect to the staff dashboard


@login_required
def time_out(request):
    # Log time out for the logged-in user
    staff_member = Staff.objects.get(user=request.user)
    time_log = TimeLog.objects.filter(staff=staff_member, date=timezone.now().date(), time_out__isnull=True).first()

    if time_log:
        time_log.time_out = timezone.now().time()
        time_log.status = 'OUT'
        time_log.save()

    return redirect('accounts/registration/staff_dashboard.html')  # Redirect to the staff dashboard


# ADD THE DASHBOARD FUNCTION HERE
@login_required
def dashboard(request):
    # Get the logged-in user's staff object
    try:
        staff = Staff.objects.get(user=request.user)
    except Staff.DoesNotExist:
        staff = None

    # Fetch the TimeLog records for the logged-in staff
    timelogs = TimeLog.objects.filter(staff=staff) if staff else []

    # Pass the TimeLog data to the template
    return render(request, 'dash_board.html', {'timelogs': timelogs})
