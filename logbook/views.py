from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.db.models import Q
from .models import LogEntry, UserProfile
from .forms import (
    UserRegisterForm, 
    LogEntryForm, 
    UserProfileForm, 
    UserUpdateForm, 
    LoginForm,
    SettingsForm
)
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('logbook:login')
        
    search_query = request.GET.get('search', '')
    if search_query:
        logs = LogEntry.objects.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        ).filter(user=request.user)
    else:
        logs = LogEntry.objects.filter(user=request.user)
    
    paginator = Paginator(logs, 10)  # Show 10 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'logbook/home.html', {
        'title': 'Home',
        'logs': page_obj
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # Create user profile
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('logbook:home')
    else:
        form = UserRegisterForm()
    return render(request, 'logbook/register.html', {'form': form})

@login_required
def create_log(request):
    if request.method == 'POST':
        form = LogEntryForm(request.POST, request.FILES)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, 'Log entry created successfully!')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('logbook:home')
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('logbook/log_form_content.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'form_html': html})
    else:
        form = LogEntryForm()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('logbook/log_form_content.html', {'form': form}, request=request)
        return JsonResponse({'form_html': html})
    return render(request, 'logbook/log_form.html', {'form': form, 'title': 'Create Log'})

@login_required
def edit_log(request, pk):
    log = get_object_or_404(LogEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = LogEntryForm(request.POST, request.FILES, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Log entry updated successfully!')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('logbook:home')
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('logbook/log_form_content.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'form_html': html})
    else:
        form = LogEntryForm(instance=log)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('logbook/log_form_content.html', {'form': form}, request=request)
        return JsonResponse({'form_html': html})
    return render(request, 'logbook/log_form.html', {'form': form, 'title': 'Edit Log'})

@login_required
def delete_log(request, pk):
    log = get_object_or_404(LogEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        log.delete()
        messages.success(request, 'Log entry deleted successfully!')
        return redirect('logbook:home')
    return render(request, 'logbook/delete_confirm.html', {'log': log})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('logbook:profile')
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('logbook/profile_form_content.html', 
                {'u_form': u_form, 'p_form': p_form}, request=request)
            return JsonResponse({'success': False, 'form_html': html})
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Profile'
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('logbook/profile_form_content.html', context, request=request)
        return JsonResponse({'form_html': html})
    return render(request, 'logbook/profile.html', context)

@login_required
def settings(request):
    # Get or create the user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Settings updated successfully!'})
            return redirect('logbook:settings')
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('logbook/settings_form_content.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'form_html': html})
    else:
        form = SettingsForm(instance=profile)
    
    context = {
        'form': form,
        'title': 'Settings'
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('logbook/settings_form_content.html', context, request=request)
        return JsonResponse({'success': True, 'form_html': html})
    return render(request, 'logbook/settings.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('logbook:home')
        
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'logbook:home')
                messages.success(request, f'Welcome back, {username}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'logbook/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('logbook:login')
