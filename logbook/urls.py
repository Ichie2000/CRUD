from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'logbook'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('log/new/', views.create_log, name='create_log'),
    path('log/<int:pk>/edit/', views.edit_log, name='edit_log'),
    path('log/<int:pk>/delete/', views.delete_log, name='delete_log'),
] 