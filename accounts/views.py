from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
from pages.models import Enrollment

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from pages.models import Course, Chapter, Page, Enrollment

@login_required
def page_detail_dashboard(request, course_slug, chapter_slug, page_slug):
    # Get the course
    course = get_object_or_404(Course, slug=course_slug)

    # Get chapter and page
    chapter = get_object_or_404(Chapter, course=course, slug=chapter_slug)
    page = get_object_or_404(Page, chapter=chapter, slug=page_slug)

    # ✅ Get enrollment for logged-in user (robust way)
    enrollment = Enrollment.objects.filter(
        user=request.user,
        course__slug=course_slug
    ).first()

    context = {
        'course': course,
        'chapter': chapter,
        'page': page,
        'enrollment': enrollment,
    }

    return render(request, 'accounts/dashboard.html', context)


# --------------------
# AUTH VIEWS
# --------------------

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')   # ✅ better UX
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')  # ✅ better UX
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# --------------------
# DASHBOARD (NEW)
# --------------------

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('course')

    return render(request, 'accounts/dashboard.html', {
        'enrollments': enrollments
    })


# --------------------
# USER PAGES
# --------------------

@login_required
def home(request):
    return redirect('dashboard')  # home → dashboard


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def view_user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'accounts/view_user_profile.html', {
        'profile_user': user
    })


@login_required
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'accounts/user_list.html', {
        'users': users
    })


# --------------------
# PROFILE EDIT
# --------------------

@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile_edit.html', {
        'u_form': u_form,
        'p_form': p_form
    })


# --------------------
# PASSWORD
# --------------------

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


# --------------------
# DELETE ACCOUNT
# --------------------

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('login')

    return render(request, 'accounts/delete_account.html')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from pages.models import Enrollment

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user, is_active=True)
    return render(request, 'accounts/dashboard.html', {'enrollments': enrollments})
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        # If form is not valid, no redirect happens, we just fall through
        # The template will have access to `form.errors`
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})

