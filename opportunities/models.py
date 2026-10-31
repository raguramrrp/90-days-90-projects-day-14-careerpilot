from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=200)
    website = models.URLField(max_length=300, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_company_per_user')
        ]

    def __str__(self):
        return self.name


class Opportunity(models.Model):
    CATEGORY_CHOICES = [
        ('Software Engineering', 'Software Engineering'),
        ('AI & Machine Learning', 'AI & Machine Learning'),
        ('Data Analytics & BI', 'Data Analytics & BI'),
        ('Full Stack Development', 'Full Stack Development'),
        ('DevOps & Cloud', 'DevOps & Cloud'),
        ('Cybersecurity', 'Cybersecurity'),
        ('QA & Testing', 'QA & Testing'),
        ('Product Management', 'Product Management'),
        ('Other', 'Other'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
        ('Part-time', 'Part-time'),
    ]

    CLASSIFICATION_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Internship', 'Internship'),
    ]

    WORK_MODE_CHOICES = [
        ('On-site', 'On-site'),
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
    ]

    SOURCE_CHOICES = [
        ('LinkedIn', 'LinkedIn'),
        ('Naukri', 'Naukri'),
        ('Indeed', 'Indeed'),
        ('Company website', 'Company website'),
        ('College placement cell', 'College placement cell'),
        ('Referral', 'Referral'),
        ('Other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    ]

    INTEREST_STATUS_CHOICES = [
        ('Saved', 'Saved'),
        ('Interested', 'Interested'),
        ('Not Interested', 'Not Interested'),
        ('Archived', 'Archived'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Software Engineering')
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES, default='Full-time')
    classification = models.CharField(max_length=50, choices=CLASSIFICATION_CHOICES, default='Full-time')
    work_mode = models.CharField(max_length=50, choices=WORK_MODE_CHOICES, default='Hybrid')
    location = models.CharField(max_length=200, blank=True)
    
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='INR')
    
    required_skills = models.TextField(blank=True, help_text="Comma-separated required skills")
    experience_requirements = models.CharField(max_length=150, blank=True, help_text="e.g. 0-1 years / Fresh graduate")
    qualification_requirements = models.CharField(max_length=150, blank=True, help_text="e.g. B.Tech CS / AI / DS")
    
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, default='LinkedIn')
    application_url = models.URLField(max_length=500, blank=True)
    posted_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    interest_status = models.CharField(max_length=30, choices=INTEREST_STATUS_CHOICES, default='Saved')
    is_accepting_applications = models.BooleanField(default=True)
    personal_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Opportunities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} @ {self.company.name}"

    @property
    def is_deadline_approaching(self):
        if not self.deadline:
            return False
        days_left = (self.deadline - timezone.now().date()).days
        return 0 <= days_left <= 3

    @property
    def is_expired(self):
        if not self.deadline:
            return False
        return self.deadline < timezone.now().date()

    @property
    def salary_display(self):
        if self.salary_min and self.salary_max:
            return f"{self.salary_currency} {self.salary_min:,.0f} - {self.salary_max:,.0f}"
        elif self.salary_min:
            return f"{self.salary_currency} {self.salary_min:,.0f}+"
        elif self.salary_max:
            return f"Up to {self.salary_currency} {self.salary_max:,.0f}"
        return "Not disclosed"
