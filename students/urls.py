from django.urls import path
from .views import student_fee_detail

urlpatterns = [
    path('my-fees/', student_fee_detail, name='student_fees'),
]
