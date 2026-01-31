from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def student_fee_detail(request):
    student = request.user.student_profile  # ✅ FIXED

    fees = student.fees.all().order_by('-paid_on')
    total_paid = sum(fee.amount for fee in fees)

    return render(request, 'students/student_fees.html', {
        'student': student,
        'fees': fees,
        'total_paid': total_paid,
    })
