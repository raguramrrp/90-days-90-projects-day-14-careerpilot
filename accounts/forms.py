from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'name@example.com'}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-input')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-input')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'headline', 'phone', 'location', 'avatar',
            'preferred_roles', 'preferred_locations',
            'preferred_employment_types', 'preferred_work_modes',
            'expected_salary', 'preferred_industries',
            'skill_profile', 'career_goals', 'follow_up_default_days', 'theme'
        ]
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. SDE Aspirant | AI & Data Science'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+91 9876543210'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City, State or Remote'}),
            'preferred_roles': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Software Engineer, Data Analyst, ML Engineer'}),
            'preferred_locations': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Bengaluru, Hyderabad, Remote'}),
            'preferred_employment_types': forms.Select(choices=[
                ('Full-time', 'Full-time'),
                ('Internship', 'Internship'),
                ('Contract', 'Contract'),
                ('Part-time', 'Part-time')
            ], attrs={'class': 'form-select'}),
            'preferred_work_modes': forms.Select(choices=[
                ('Hybrid', 'Hybrid'),
                ('Remote', 'Remote'),
                ('On-site', 'On-site')
            ], attrs={'class': 'form-select'}),
            'expected_salary': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 10 LPA / $85,000'}),
            'preferred_industries': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'FinTech, SaaS, Healthcare, AI'}),
            'skill_profile': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Python, Django, PostgreSQL, Scikit-learn, React'}),
            'career_goals': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Targeting 2 full-time offers before campus drive ends...'}),
            'follow_up_default_days': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 60}),
            'theme': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-file-input'}),
        }
