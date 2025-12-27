from .models import Enrollment

def is_enrolled(user, course):
    if not user.is_authenticated:
        return False
    return Enrollment.objects.filter(
        user=user,
        course=course,
        is_active=True
    ).exists()
