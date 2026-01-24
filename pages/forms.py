# forms.py
from django import forms
from .models import AssignmentSubmission

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ('answer_text', 'answer_file')