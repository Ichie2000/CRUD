from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import LogEntry, UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LogEntryForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
        }
        labels = {
            'profile_picture': 'Profile Picture',
            'bio': 'About Me'
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )

class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'theme',
            'items_per_page',
            'show_recent_first',
            'enable_notifications',
            'notification_preference',
            'auto_save_interval',
            'default_view'
        ]
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'items_per_page': forms.Select(attrs={'class': 'form-control'}),
            'notification_preference': forms.Select(attrs={'class': 'form-control'}),
            'auto_save_interval': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '60'
            }),
            'default_view': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'theme': 'Application Theme',
            'items_per_page': 'Items Per Page',
            'show_recent_first': 'Show Recent Logs First',
            'enable_notifications': 'Enable Notifications',
            'notification_preference': 'Notification Level',
            'auto_save_interval': 'Auto-save Interval (minutes)',
            'default_view': 'Default View Mode'
        }
        help_texts = {
            'theme': 'Choose your preferred color theme',
            'items_per_page': 'Number of logs to display per page',
            'show_recent_first': 'If checked, newest logs will appear at the top',
            'enable_notifications': 'Receive notifications about your logs',
            'notification_preference': 'Choose which activities to be notified about',
            'auto_save_interval': 'Set to 0 to disable auto-save',
            'default_view': 'Choose how your logs are displayed by default'
        } 