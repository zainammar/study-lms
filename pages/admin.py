from django.contrib import admin
from .models import Course, Chapter, Page, Enrollment, Assignment, AssignmentSubmission
from django.contrib import admin
from .models import LiveClass


@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'start_time', 'end_time')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('-start_time',)

# Inline for Pages under Chapter
class PageInline(admin.TabularInline):
    model = Page
    extra = 1

# Inline for Chapters under Course
class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

# Admin for Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChapterInline]
    list_display = ('title',)
    search_fields = ('title',)

# Admin for Chapter
@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PageInline]
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')

# Admin for Page
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'chapter', 'order')
    list_filter = ('chapter',)
    ordering = ('chapter', 'order')

# Admin for Enrollment
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('user__username', 'course__title')
    ordering = ('-enrolled_at',)

autocomplete_fields = ['user', 'course']





@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'chapter', 'due_date', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('title', 'course__title')
    ordering = ('-created_at',)


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'is_checked', 'marks')
    list_filter = ('is_checked', 'assignment')
    search_fields = ('student__username',)
    ordering = ('-submitted_at',)