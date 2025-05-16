from django.contrib import admin
from .models import LogEntry, UserProfile

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'bio')
    search_fields = ('user__username', 'user__email', 'bio')
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
