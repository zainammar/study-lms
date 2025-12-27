from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Chapter, Page, Enrollment
from django.contrib import messages

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'pages/course_list.html', {'courses': courses})

def chapter_list(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    return render(request, 'pages/chapter_list.html', {'course': course})

@login_required
def page_detail(request, course_slug, chapter_slug, page_slug):
    course = get_object_or_404(Course, slug=course_slug)
    chapter = get_object_or_404(Chapter, course=course, slug=chapter_slug)
    page = get_object_or_404(Page, chapter=chapter, slug=page_slug)

    # Check if user is enrolled
    if not Enrollment.objects.filter(user=request.user, course=course, is_active=True).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('course_list')

    return render(request, 'pages/page_detail.html', {
        'course': course,
        'chapter': chapter,
        'page': page
    })
