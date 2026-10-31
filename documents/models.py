import os
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings


def validate_document_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    allowed_exts = getattr(settings, 'ALLOWED_DOCUMENT_EXTENSIONS', ['.pdf', '.doc', '.docx', '.txt', '.png', '.jpg', '.jpeg'])
    if ext not in allowed_exts:
        raise ValidationError(f"Unsupported file format '{ext}'. Allowed: {', '.join(allowed_exts)}")
    
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 5 * 1024 * 1024)
    if file.size > max_size:
        raise ValidationError(f"File size exceeds limit of {max_size // (1024 * 1024)}MB.")


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('Resume', 'Resume'),
        ('Cover Letter', 'Cover Letter'),
        ('Certificate', 'Certificate'),
        ('Academic Transcript', 'Academic Transcript'),
        ('Internship Certificate', 'Internship Certificate'),
        ('Other', 'Other Supporting Document'),
    ]

    RESUME_CATEGORIES = [
        ('General', 'General Purpose'),
        ('Data Analyst', 'Data Analyst / BI'),
        ('Python Developer', 'Python Developer'),
        ('Software Engineer', 'Software Engineer / SDE'),
        ('Software Tester', 'QA / Software Tester'),
        ('Internship', 'Internship Targeted'),
        ('None', 'Not Applicable'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, default='Resume')
    resume_category = models.CharField(max_length=50, choices=RESUME_CATEGORIES, default='General')
    file = models.FileField(upload_to='documents/%Y/%m/', validators=[validate_document_file])
    file_size = models.PositiveIntegerField(default=0, help_text="File size in bytes")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.document_type})"

    def save(self, *args, **kwargs):
        if self.file and hasattr(self.file, 'size'):
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    @property
    def file_extension(self):
        return os.path.splitext(self.file.name)[1].lower().replace('.', '')

    @property
    def formatted_size(self):
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        return f"{self.file_size / (1024 * 1024):.1f} MB"
