from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def staff_dashboard(request):
    return render(request, 'registration/staff_dashboard.html')
def time_in(request):
    return render(request, 'registration/time_in.html')
def time_out(request):
    return render(request, 'registration/time_out.html')