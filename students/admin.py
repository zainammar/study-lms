from django.contrib import admin
from .models import Student, Fee

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gr_number', 'class_name', 'section_name')
    search_fields = ('first_name', 'last_name', 'gr_number')


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'paid_on')
    list_filter = ('paid_on',)
