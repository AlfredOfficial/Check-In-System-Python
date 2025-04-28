from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
   path('admin/', admin.site.urls),
   path('login/', auth_views.LoginView.as_view(), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   path('staff_dashboard/', auth_views.TemplateView.as_view(template_name='staff_dashboard.html'), name='staff_dashboard'),
]
