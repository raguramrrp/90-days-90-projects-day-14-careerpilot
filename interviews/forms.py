from django import forms
from .models import Interview, InterviewChecklistItem
from applications.models import Application


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            'application', 'round_number', 'round_title', 'interview_date', 'interview_time',
            'mode', 'meeting_url', 'location', 'interviewer_names', 'interviewer_titles',
            'preparation_notes', 'topics_to_prepare',
            'outcome', 'feedback', 'questions_asked', 'topics_covered',
            'personal_answers', 'areas_to_improve', 'next_round_date'
        ]
        widgets = {
            'application': forms.Select(attrs={'class': 'form-select'}),
            'round_number': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 20}),
            'round_title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Round 1: Coding & Data Structures'}),
            'interview_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'interview_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'mode': forms.Select(attrs={'class': 'form-select'}),
            'meeting_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://meet.google.com/xyz or Zoom link'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Office Address (for offline rounds)'}),
            'interviewer_names': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Names of interviewers'}),
            'interviewer_titles': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Senior Tech Lead, Engineering Manager'}),
            'preparation_notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Notes on project talking points, system design considerations...'}),
            'topics_to_prepare': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'e.g. Trees, Graphs, Indexing in PostgreSQL, REST APIs'}),
            'outcome': forms.Select(attrs={'class': 'form-select'}),
            'feedback': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Recruiter / panel feedback'}),
            'questions_asked': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Specific questions asked during the round'}),
            'topics_covered': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Topics covered during discussion'}),
            'personal_answers': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'How you approached the problem, algorithms used, code written'}),
            'areas_to_improve': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Topics or concepts that need revision'}),
            'next_round_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['application'].queryset = Application.objects.filter(
                user=user,
                is_archived=False
            ).select_related('opportunity', 'opportunity__company')


class InterviewChecklistItemForm(forms.ModelForm):
    class Meta:
        model = InterviewChecklistItem
        fields = ['item_text']
        widgets = {
            'item_text': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Add custom checklist item...'})
        }
