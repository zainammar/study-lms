from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Chapter, Page, Enrollment
from django.http import HttpResponseForbidden

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Assignment
from .forms import AssignmentSubmissionForm


# def course_list(request):
#     courses = Course.objects.all()
#     return render(request, 'pages/course_list.html', {'courses': courses})


def course_list(request):
    return HttpResponseForbidden("Access to this page is blocked.")

def chapter_list(request, course_slug):
    course = get_object_or_404(
        Course.objects.prefetch_related('chapters__pages'),
        slug=course_slug
    )
    return render(request, 'pages/chapter_list.html', {'course': course})


@login_required
def page_detail(request, course_slug, chapter_slug, page_slug):
    # Load course with chapters & pages for sidebar
    course = get_object_or_404(
        Course.objects.prefetch_related('chapters__pages'),
        slug=course_slug
    )

    chapter = get_object_or_404(
        Chapter,
        course=course,
        slug=chapter_slug
    )

    page = get_object_or_404(
        Page,
        chapter=chapter,
        slug=page_slug
    )

    # Enrollment check
    if not Enrollment.objects.filter(
        user=request.user,
        course=course,
        is_active=True
    ).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('course_list')

    return render(request, 'pages/page_detail.html', {
        'course': course,   # sidebar
        'chapter': chapter, # optional (active chapter)
        'page': page        # main content
    })



@login_required
def assignment_list(request, course_id):
    assignments = Assignment.objects.filter(course_id=course_id, is_active=True)
    return render(request, 'pages/assignment_list.html', {
        'assignments': assignments
    })


@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect('assignment_list', course_id=assignment.course.id)
    else:
        form = AssignmentSubmissionForm()

    return render(request, 'pages/submit_assignment.html', {
        'assignment': assignment,
        'form': form
    })
