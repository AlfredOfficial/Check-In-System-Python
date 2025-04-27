from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import TimeLog

class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')  # Redirect to admin dashboard
            elif user.is_staff:
                return redirect('registration/staff_dashboard')
            else:
                return redirect('home')
        return render(request, 'registration/login.html', {'form': form})


# nag add then ni function na pero libog pa
@login_required
def staff_dashboard(request):
    if request.user.is_staff:
        # Fetch the time logs for the logged-in staff member
        time_logs = TimeLog.objects.filter(staff__staff_username=request.user.username)
        # pass timelogs to the template
        return render(request, 'registration/staff_dashboard.html', {'time_logs': time_logs})
    else:
        return redirect('home')
