from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'resume_category', 'file', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Ragu_Ram_SDE_Resume_v2.pdf'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'resume_category': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-file-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Version notes, targeted roles, customized keywords...'}),
        }


class DocumentEditForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'resume_category', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'resume_category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
