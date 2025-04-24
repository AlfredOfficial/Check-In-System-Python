from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import CustomAuthenticationForm  # Import the custom form
from .models import UserTimeLog  # Import the UserTimeLog model

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)  # Use the custom form
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:  # Check if the user is an admin
                return redirect('/admin/')  # Redirect to Django admin interface
            elif user.groups.filter(name='Interns').exists():  # Check if the user is in the Interns group
                return redirect('intern_dashboard')  # Redirect to intern dashboard
            else:
                return redirect('home')  # Redirect to a default page for other users
        else:
            return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = CustomAuthenticationForm()  # Use the custom form
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def intern_dashboard(request): # This view is for the intern dashboard
    
    # Check if the logged-in user is part of the "Interns" group
    if request.user.groups.filter(name='Interns').exists():
        # Fetch time logs for the logged-in intern
        time_logs = UserTimeLog.objects.filter(user=request.user)
        return render(request, 'accounts/intern_dashboard.html', {'time_logs': time_logs})
    else:
        # Redirect non-interns to the homepage or another page
        return redirect('home')