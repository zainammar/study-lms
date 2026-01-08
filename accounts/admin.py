from django.contrib import admin
from .models import Profile
from django.contrib import admin

admin.site.site_header = "Study LMS Administration"
admin.site.site_title = "Study LMS Admin"
admin.site.index_title = "Welcome to Study LMS Admin Panel"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'phone']
    search_fields = ['user__username', 'location']
    list_filter = ['location']