from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import os

class LogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_logs')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='log_images/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Log Entries'

    def __str__(self):
        return f"{self.title} - {self.user.username}"

def get_default_profile_pic():
    return 'profile_pics/default.jpg'

class UserProfile(models.Model):
    THEME_CHOICES = [
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme'),
        ('green', 'Green Theme')
    ]
    
    ITEMS_PER_PAGE_CHOICES = [
        (5, '5 items'),
        (10, '10 items'),
        (20, '20 items'),
        (50, '50 items')
    ]

    NOTIFICATION_PREFERENCES = [
        ('all', 'All Activities'),
        ('important', 'Important Only'),
        ('none', 'No Notifications')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default=get_default_profile_pic,
        null=True,
        blank=True
    )
    bio = models.TextField(max_length=500, blank=True)
    
    # App Settings
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    items_per_page = models.IntegerField(choices=ITEMS_PER_PAGE_CHOICES, default=10)
    show_recent_first = models.BooleanField(default=True, help_text='Show most recent logs first')
    enable_notifications = models.BooleanField(default=True)
    notification_preference = models.CharField(max_length=10, choices=NOTIFICATION_PREFERENCES, default='all')
    auto_save_interval = models.IntegerField(default=5, help_text='Auto-save interval in minutes (0 to disable)')
    default_view = models.CharField(max_length=10, choices=[('list', 'List View'), ('grid', 'Grid View')], default='list')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return os.path.join(settings.MEDIA_URL, 'profile_pics/default.jpg')
