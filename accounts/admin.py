from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'phone']
    search_fields = ['user__username', 'location']
    list_filter = ['location']


admin.site.site_header = "Study LMS Admin"
admin.site.site_title = "Study LMS"
admin.site.index_title = "Welcome to Study LMS Dashboard"