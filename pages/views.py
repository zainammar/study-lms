from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Chapter, Page, Enrollment
from django.http import HttpResponseForbidden

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Assignment
from .models import Course
from django.contrib.auth.decorators import login_required
from .models import Course, Assignment, AssignmentSubmission
from .forms import AssignmentSubmissionForm
from .models import Page, AssignmentSubmission
from .models import AssignmentSubmission



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, LiveClass

@login_required
def live_classes(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    enrollment = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).first()

    # ❌ Not enrolled OR expired
    if not enrollment or not enrollment.is_active:
        return render(request, 'pages/course_expired.html', {
            'course': course
        })

    live_classes = LiveClass.objects.filter(course=course).order_by('start_time')

    return render(request, 'pages/live_classes.html', {
        'course': course,
        'live_classes': live_classes,
        'enrollment': enrollment
    })

def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    assignments = course.assignments.all()
    return render(request, 'pages/page_detail.html', {
        'course': course,
        'assignments': assignments
    })


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



def course_detail(request, slug):
    course = Course.objects.get(slug=slug)
    assignments = course.assignments.all()

    return render(request, 'page_detail.html', {
        'course': course,
        'assignments': assignments
    })




# views.py
def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    assignments = course.assignments.all()
    return render(request, 'pages/page_detail.html', {
        'course': course,
        'assignments': assignments
    })




# new

# views.py
@login_required
def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    assignments = course.assignments.all()

    for assignment in assignments:
        try:
            submission = AssignmentSubmission.objects.get(assignment=assignment, student=request.user)
            assignment.submitted = True
        except AssignmentSubmission.DoesNotExist:
            assignment.submitted = False

    if request.method == 'POST':
        print("Form submitted")  # Add this line
        assignment_id = request.POST.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect('page_detail', course_slug=course_slug)
        else:
            print(form.errors)  # Add this line to check form errors
    else:
        form = AssignmentSubmissionForm()

    return render(request, 'pages/page_detail.html', {
        'course': course,
        'assignments': assignments,
        'form': form
    })


@login_required
def page_detail(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    submissions = AssignmentSubmission.objects.filter(student=request.user, assignment__course=page.chapter.course)
    return render(request, 'pages/page_detail.html', {
        'page': page,
        'submissions': submissions
    })




@login_required
def results(request):
    submissions = AssignmentSubmission.objects.filter(student=request.user)
    return render(request, 'pages/results.html', {
        'submissions': submissions
    })

@login_required
def page_detail(request, course_slug, chapter_slug, page_slug):
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

    if not Enrollment.objects.filter(
        user=request.user,
        course=course,
        is_active=True
    ).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('course_list')

    return render(request, 'pages/page_detail.html', {
        'course': course,
        'chapter': chapter,
        'page': page
    })


@login_required
def page_detail(request, course_slug, chapter_slug, page_slug):
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

    assignments = Assignment.objects.filter(course=course)

    if not Enrollment.objects.filter(
        user=request.user,
        course=course,
        is_active=True
    ).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('course_list')

    return render(request, 'pages/page_detail.html', {
        'course': course,
        'chapter': chapter,
        'page': page,
        'assignments': assignments  # Add assignments to the context
    })

@login_required
def page_detail(request, course_slug, chapter_slug, page_slug):
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

    assignments = Assignment.objects.filter(course=course)
    submissions = AssignmentSubmission.objects.filter(student=request.user, assignment__course=course)

    if not Enrollment.objects.filter(
        user=request.user,
        course=course,
        is_active=True
    ).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('course_list')

    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect('page_detail', course_slug=course_slug, chapter_slug=chapter_slug, page_slug=page_slug)
    else:
        form = AssignmentSubmissionForm()

    return render(request, 'pages/page_detail.html', {
        'course': course,
        'chapter': chapter,
        'page': page,
        'assignments': assignments,
        'submissions': submissions,
        'form': form,
    })



@login_required
def page_detail(request, course_slug, chapter_slug, page_slug):
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

    assignments = Assignment.objects.filter(course=course)
    submissions = AssignmentSubmission.objects.filter(student=request.user, assignment__course=course)

    for assignment in assignments:
        assignment.submitted = submissions.filter(assignment=assignment).exists()

    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        try:
            submission = AssignmentSubmission.objects.get(assignment=assignment, student=request.user)
        except AssignmentSubmission.DoesNotExist:
            submission = AssignmentSubmission(assignment=assignment, student=request.user)
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('page_detail', course_slug=course_slug, chapter_slug=chapter_slug, page_slug=page_slug)
    else:
        form = AssignmentSubmissionForm()

    return render(request, 'pages/page_detail.html', {
        'course': course,
        'chapter': chapter,
        'page': page,
        'assignments': assignments,
        'submissions': submissions,
        'form': form,
    })