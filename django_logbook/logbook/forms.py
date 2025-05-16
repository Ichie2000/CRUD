from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm
from django.contrib.auth.models import User
from .models import Record, Profile

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['title', 'description', 'date', 'time', 'tags']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'phone_number', 'department']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['theme', 'language', 'timezone', 'items_per_page']
        widgets = {
            'theme': forms.Select(choices=[
                ('light', 'Light'),
                ('dark', 'Dark'),
                ('system', 'System Default')
            ]),
            'language': forms.Select(choices=[
                ('en', 'English'),
                ('es', 'Spanish'),
                ('fr', 'French')
            ]),
            'items_per_page': forms.NumberInput(attrs={'min': 5, 'max': 100})
        }

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email_notifications', 'browser_notifications', 'notification_frequency']
        widgets = {
            'notification_frequency': forms.Select(choices=[
                ('immediately', 'Immediately'),
                ('daily', 'Daily Digest'),
                ('weekly', 'Weekly Digest'),
                ('never', 'Never')
            ])
        }

class PasswordChangeForm(AuthPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class SearchForm(forms.Form):
    q = forms.CharField(label='Search', required=False)
    search_title = forms.BooleanField(required=False)
    search_description = forms.BooleanField(required=False)
    search_tags = forms.BooleanField(required=False) 