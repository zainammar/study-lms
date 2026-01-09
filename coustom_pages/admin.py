from django.contrib import admin
from .models import PageLink

@admin.register(PageLink)
class PageLinkAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'slug', 'title', 'menu_order')
    prepopulated_fields = {'slug': ('page_name',)}
    ordering = ('menu_order',)  # Default admin order
