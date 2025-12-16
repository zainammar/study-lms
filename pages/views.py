from django.shortcuts import render, get_object_or_404
from .models import Course, Chapter, Page


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'pages/course_list.html', {'courses': courses})


def chapter_list(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    return render(request, 'pages/chapter_list.html', {'course': course})


def page_detail(request, course_slug, chapter_slug, page_slug):
    course = get_object_or_404(Course, slug=course_slug)
    chapter = get_object_or_404(Chapter, course=course, slug=chapter_slug)
    page = get_object_or_404(Page, chapter=chapter, slug=page_slug)

    return render(request, 'pages/page_detail.html', {
        'course': course,
        'chapter': chapter,
        'page': page
    })
