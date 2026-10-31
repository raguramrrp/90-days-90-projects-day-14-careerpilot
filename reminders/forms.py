from django import forms
from django.utils import timezone
from .models import Reminder
from applications.models import Application
from opportunities.models import Opportunity


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = [
            'title', 'reminder_type', 'due_date', 'due_time',
            'priority', 'application', 'opportunity', 'description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Email HR regarding Round 2 update'}),
            'reminder_type': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'application': forms.Select(attrs={'class': 'form-select'}),
            'opportunity': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Context, email template, questions to ask, or notes...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['due_date'].initial = timezone.now().date()
        if user:
            self.fields['application'].queryset = Application.objects.filter(
                user=user, is_archived=False
            ).select_related('opportunity', 'opportunity__company')
            self.fields['opportunity'].queryset = Opportunity.objects.filter(user=user)
