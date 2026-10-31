from django import forms
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import Application, ApplicationNote
from opportunities.models import Opportunity
from documents.models import Document


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'opportunity', 'status', 'application_date', 'application_method',
            'submitted_resume', 'expected_salary', 'offered_salary',
            'follow_up_date', 'recruiter_name', 'recruiter_email', 'recruiter_phone',
            'referral_name', 'referral_details', 'notes',
            'rejection_reason', 'withdrawal_reason'
        ]
        widgets = {
            'opportunity': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'application_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'application_method': forms.Select(attrs={'class': 'form-select'}),
            'submitted_resume': forms.Select(attrs={'class': 'form-select'}),
            'expected_salary': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 900000'}),
            'offered_salary': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 1000000'}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'recruiter_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Recruiter / Talent Partner'}),
            'recruiter_email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'recruiter@company.com'}),
            'recruiter_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+91 ...'}),
            'referral_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Referrer name & designation'}),
            'referral_details': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Referral ID, relation, or message sent'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Cover letter excerpts, custom portfolio link, portal login details...'}),
            'rejection_reason': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Feedback or rejection rationale if provided'}),
            'withdrawal_reason': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Why you chose to withdraw application'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user

        if user:
            # When creating a new application, default to opportunities without active applications
            if not self.instance.pk:
                active_opp_ids = Application.objects.filter(
                    user=user,
                    is_archived=False
                ).values_list('opportunity_id', flat=True)

                initial_opp = self.initial.get('opportunity')
                initial_opp_id = initial_opp.pk if hasattr(initial_opp, 'pk') else initial_opp

                available_opps = Opportunity.objects.filter(user=user)
                if initial_opp_id:
                    available_opps = available_opps.filter(
                        Q(id=initial_opp_id) | ~Q(id__in=active_opp_ids)
                    )
                else:
                    available_opps = available_opps.exclude(id__in=active_opp_ids)

                self.fields['opportunity'].queryset = available_opps
            else:
                self.fields['opportunity'].queryset = Opportunity.objects.filter(user=user)

            self.fields['submitted_resume'].queryset = Document.objects.filter(
                user=user,
                document_type__in=['Resume', 'Cover Letter']
            )

            # Default follow-up date suggestion if creating new application
            if not self.instance.pk and hasattr(user, 'profile'):
                default_days = user.profile.follow_up_default_days or 7
                self.fields['follow_up_date'].initial = timezone.now().date() + timedelta(days=default_days)

    def clean(self):
        cleaned_data = super().clean()
        opportunity = cleaned_data.get('opportunity')
        if opportunity and getattr(self, 'user', None):
            qs = Application.objects.filter(
                user=self.user,
                opportunity=opportunity,
                is_archived=False
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error(
                    'opportunity',
                    f"An active application for '{opportunity.title}' at {opportunity.company.name} already exists. You can edit the existing application instead."
                )
        return cleaned_data


class ApplicationNoteForm(forms.ModelForm):
    class Meta:
        model = ApplicationNote
        fields = ['note_text']
        widgets = {
            'note_text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Add update note, recruiter call notes, or submission details...'
            })
        }
