from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'), # Now 'views' is defined
    path('profile/', account_views.profile, name='profile'), # Now 'account_views' is defined
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')), # Includes login, logout, password reset etc.
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # Keep this commented if using include('django.contrib.auth.urls')
    path('clients/', include('clients.urls')),
    path('cases/', include('cases.urls')),
    path('appointments/', include('appointments.urls')),
    path('documents/', include('documents.urls')),
    path('register/', account_views.register, name='register'), 

]


