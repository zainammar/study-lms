# students/views.py
from django.shortcuts import render, redirect # Import redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Fee

@login_required
def student_fee_detail(request):
    student = getattr(request.user, 'student_profile', None)

    if not student:
        return redirect('/')

    fees = student.fees.all().order_by('-paid_on')
    total_paid = sum(fee.amount for fee in fees)

    return render(request, 'students/student_fees.html', {
        'student': student,
        'fees': fees,
        'total_paid': total_paid,
        'has_fees': fees.exists(),
    })