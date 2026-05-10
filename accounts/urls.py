from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', RedirectView.as_view(pattern_name='account_signup', permanent=False), name='signup'),
    path('login/', RedirectView.as_view(pattern_name='account_login', permanent=False), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('validate-email/', views.validate_email, name='validate_email'),
    path('validate-username/', views.validate_username, name='validate_username'),
    
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),

    path('setup/', views.profile_setup, name='profile_setup'),
]