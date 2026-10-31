from django import forms
from django.utils import timezone
from .models import CareerTask, CareerGoal
from opportunities.models import Opportunity
from applications.models import Application


class CareerTaskForm(forms.ModelForm):
    class Meta:
        model = CareerTask
        fields = [
            'title', 'category', 'priority', 'due_date', 'due_time',
            'related_opportunity', 'related_application', 'description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Solve 2 Dynamic Programming problems on LeetCode'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'related_opportunity': forms.Select(attrs={'class': 'form-select'}),
            'related_application': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Specific objectives, problem links, or checklist notes...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['due_date'].initial = timezone.now().date()
        if user:
            self.fields['related_opportunity'].queryset = Opportunity.objects.filter(user=user)
            self.fields['related_application'].queryset = Application.objects.filter(
                user=user, is_archived=False
            ).select_related('opportunity', 'opportunity__company')


class CareerGoalForm(forms.ModelForm):
    class Meta:
        model = CareerGoal
        fields = ['goal_type', 'category', 'title', 'target_count', 'period_start_date', 'period_end_date', 'notes']
        widgets = {
            'goal_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Apply to 5 Quality SDE Roles this week'}),
            'target_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 100}),
            'period_start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'period_end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Action strategy or weekly focus...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            today = timezone.now().date()
            self.fields['period_start_date'].initial = today
            self.fields['period_end_date'].initial = today + timezone.timedelta(days=7)
