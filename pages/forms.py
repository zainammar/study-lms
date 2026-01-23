from django import forms
from .models import AssignmentSubmission

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['answer_text', 'answer_file']

    def clean_answer_file(self):
        file = self.cleaned_data.get('answer_file')
        if file:
            if not file.name.lower().endswith(('.pdf', '.doc', '.docx')):
                raise forms.ValidationError("Only PDF or Word files allowed.")
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 10MB.")
        return file
