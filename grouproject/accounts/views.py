from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm  # Import the custom form

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)  # Use the custom form
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to the home page or dashboard
        else:
            return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = CustomAuthenticationForm()  # Use the custom form
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')