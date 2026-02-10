# students/views.py
from django.shortcuts import render, redirect # Import redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Fee

@login_required
def student_fee_detail(request):
    try:
        student = request.user.student_profile
        fees = student.fees.all().order_by('-paid_on')
        total_paid = sum(fee.amount for fee in fees)
        
        has_fees = fees.exists() 

        return render(request, 'students/student_fees.html', {
            'student': student,
            'fees': fees,
            'total_paid': total_paid,
            'has_fees': has_fees,
        })
    except Student.DoesNotExist:
        # If no Student profile exists, redirect to the home page
        return redirect('/') # Or redirect to a named URL, e.g., 'home' or 'index'