from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('intern_dashboard/', views.intern_dashboard, name='intern_dashboard'), #nag add ng path para sa intern dashboard
]
