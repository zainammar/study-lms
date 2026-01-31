from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    gr_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    father_name = models.CharField(max_length=100, null=True, blank=True)
    class_name = models.CharField(max_length=50)
    section_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Fee(models.Model):
    student = models.ForeignKey(
        Student,
        related_name='fees',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(auto_now_add=True)
    remarks = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.student} - {self.amount}"
