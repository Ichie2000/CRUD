from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Record, Profile
from .forms import (
    RecordForm, 
    UserRegistrationForm, 
    UserProfileForm, 
    UserPreferencesForm,
    NotificationSettingsForm,
    PasswordChangeForm
)

class CustomLoginView(LoginView):
    template_name = 'logbook/login.html'
    redirect_authenticated_user = True

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'logbook/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'logbook/register.html', {'form': form})

@login_required
def home_view(request):
    records = Record.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'logbook/home.html', {'records': records})

@login_required
def input_log_view(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Log entry saved successfully!')
            return redirect('home')
    else:
        form = RecordForm()
    return render(request, 'logbook/input_log.html', {'form': form})

@login_required
def edit_log_view(request, pk):
    record = get_object_or_404(Record, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Log entry updated successfully!')
            return redirect('home')
    else:
        form = RecordForm(instance=record)
    return render(request, 'logbook/input_log.html', {'form': form})

@login_required
def delete_log_view(request, pk):
    record = get_object_or_404(Record, pk=pk, user=request.user)
    record.delete()
    messages.success(request, 'Log entry deleted successfully!')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    recent_logs = Record.objects.filter(user=request.user).order_by('-date', '-time')[:5]
    
    return render(request, 'logbook/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'recent_logs': recent_logs
    })

@login_required
def settings_view(request):
    return render(request, 'logbook/settings.html', {
        'password_form': PasswordChangeForm(user=request.user),
        'preferences_form': UserPreferencesForm(instance=request.user.profile),
        'notifications_form': NotificationSettingsForm(instance=request.user.profile)
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('settings')
    return redirect('settings')

@login_required
def update_preferences(request):
    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferences updated successfully!')
    return redirect('settings')

@login_required
def update_notifications(request):
    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification settings updated successfully!')
    return redirect('settings')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('login')
    return redirect('settings')

@login_required
def search_view(request):
    query = request.GET.get('q', '')
    search_title = request.GET.get('search_title', False)
    search_description = request.GET.get('search_description', False)
    search_tags = request.GET.get('search_tags', False)
    
    if query:
        filters = Q()
        if search_title:
            filters |= Q(title__icontains=query)
        if search_description:
            filters |= Q(description__icontains=query)
        if search_tags:
            filters |= Q(tags__icontains=query)
            
        if not any([search_title, search_description, search_tags]):
            filters = Q(title__icontains=query) | Q(description__icontains=query)
            
        results = Record.objects.filter(filters, user=request.user).order_by('-date', '-time')
    else:
        results = Record.objects.none()
    
    paginator = Paginator(results, 10)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'results': [{
                'title': record.title,
                'description': record.description,
                'created_at': record.date.strftime('%b %d, %Y'),
                'id': record.id
            } for record in results]
        })
    
    return render(request, 'logbook/search.html', {'results': results}) 