from django import forms
from .models import Opportunity, Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'website', 'location', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Company Name (e.g. Google, Microsoft, Razorpay)'}),
            'website': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://careers.company.com'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Headquarters / Office City'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Brief description of the organization'}),
        }


class OpportunityForm(forms.ModelForm):
    company_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Company Name (e.g. Amazon, Zoho, Infosys)',
            'autocomplete': 'off',
            'id': 'id_company_name'
        })
    )
    company_website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://company.com/careers'})
    )

    class Meta:
        model = Opportunity
        fields = [
            'title', 'category', 'employment_type', 'classification',
            'work_mode', 'location', 'salary_min', 'salary_max', 'salary_currency',
            'required_skills', 'experience_requirements', 'qualification_requirements',
            'source', 'application_url', 'posted_date', 'deadline',
            'priority', 'interest_status', 'is_accepting_applications',
            'description', 'personal_notes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Job Title (e.g. Associate Software Engineer)', 'id': 'id_opportunity_title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'classification': forms.Select(attrs={'class': 'form-select'}),
            'work_mode': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Job Location (e.g. Bengaluru, Remote)'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Min (e.g. 600000)'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Max (e.g. 1200000)'}),
            'salary_currency': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'INR, USD, EUR'}),
            'required_skills': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Python, Django, React, SQL'}),
            'experience_requirements': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '0-2 years / 2024-2025 graduates'}),
            'qualification_requirements': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'B.Tech/BE in CS, AI, DS, IT, ECE or equivalent'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'application_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://jobs.lever.co/...'}),
            'posted_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'deadline': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'interest_status': forms.Select(attrs={'class': 'form-select'}),
            'is_accepting_applications': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Paste job summary, responsibilities, or eligibility...'}),
            'personal_notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Notes on company culture, referral contact, prep topics...'}),
        }

    def clean_salary_currency(self):
        curr = self.cleaned_data.get('salary_currency')
        return curr or 'INR'

    def clean_source(self):
        src = self.cleaned_data.get('source')
        return src or 'LinkedIn'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if 'source' in self.fields:
            self.fields['source'].required = False
            self.fields['source'].initial = 'LinkedIn'
        if 'salary_currency' in self.fields:
            self.fields['salary_currency'].required = False
            self.fields['salary_currency'].initial = 'INR'
        if self.instance and self.instance.pk and self.instance.company:
            self.fields['company_name'].initial = self.instance.company.name
            self.fields['company_website'].initial = self.instance.company.website
