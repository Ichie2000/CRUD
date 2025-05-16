from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logbook/login.html'), name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Main application URLs
    path('', views.home_view, name='home'),
    path('input/', views.input_log_view, name='input_log'),
    path('edit/<int:pk>/', views.edit_log_view, name='edit_log'),
    path('delete/<int:pk>/', views.delete_log_view, name='delete_log'),
    
    # User profile and settings URLs
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/password/', views.change_password, name='change_password'),
    path('settings/preferences/', views.update_preferences, name='update_preferences'),
    path('settings/notifications/', views.update_notifications, name='update_notifications'),
    path('settings/delete-account/', views.delete_account, name='delete_account'),
    
    # Search URL
    path('search/', views.search_view, name='search'),
    
    # Password reset URLs
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='logbook/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='logbook/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='logbook/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='logbook/password_reset_complete.html'),
         name='password_reset_complete'),
] 