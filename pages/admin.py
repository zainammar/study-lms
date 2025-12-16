from django.contrib import admin
from .models import Course, Chapter, Page


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1


class PageInline(admin.TabularInline):
    model = Page
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChapterInline]


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PageInline]
    list_display = ('title', 'course', 'order')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'chapter', 'order')
