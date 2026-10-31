from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from opportunities.models import Opportunity
from documents.models import Document


class Application(models.Model):
    STATUS_CHOICES = [
        ('Saved', 'Saved'),
        ('Interested', 'Interested'),
        ('Applied', 'Applied'),
        ('Assessment', 'Assessment'),
        ('Technical Interview', 'Technical Interview'),
        ('HR Interview', 'HR Interview'),
        ('Offer Received', 'Offer Received'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Withdrawn', 'Withdrawn'),
    ]

    METHOD_CHOICES = [
        ('Company Portal', 'Company Career Portal'),
        ('LinkedIn Easy Apply', 'LinkedIn Easy Apply'),
        ('Naukri FastForward', 'Naukri'),
        ('Email', 'Direct Recruiter Email'),
        ('College Placement Cell', 'College Placement Cell'),
        ('Referral', 'Employee Referral'),
        ('Job Board', 'Other Job Board'),
        ('Other', 'Other Method'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Applied')
    application_date = models.DateField(default=timezone.now)
    application_method = models.CharField(max_length=50, choices=METHOD_CHOICES, default='Company Portal')
    
    recruiter_name = models.CharField(max_length=150, blank=True)
    recruiter_email = models.EmailField(blank=True)
    recruiter_phone = models.CharField(max_length=50, blank=True)
    referral_name = models.CharField(max_length=150, blank=True)
    referral_details = models.TextField(blank=True)
    
    submitted_resume = models.ForeignKey(
        Document, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='applications_as_resume'
    )
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    offered_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    
    rejection_reason = models.TextField(blank=True)
    withdrawal_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_archived = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-application_date', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'opportunity'],
                condition=models.Q(is_archived=False),
                name='unique_active_application_per_opportunity'
            )
        ]

    def __str__(self):
        return f"{self.opportunity.title} @ {self.opportunity.company.name} [{self.status}]"

    def change_status(self, new_status, notes=""):
        if self.status != new_status:
            prev_status = self.status
            self.status = new_status
            self.save(update_fields=['status', 'updated_at'])
            ApplicationStatusHistory.objects.create(
                application=self,
                previous_status=prev_status,
                new_status=new_status,
                notes=notes
            )
            return True
        return False

    @property
    def is_terminal_state(self):
        return self.status in ('Accepted', 'Rejected', 'Withdrawn')

    @property
    def is_in_progress(self):
        return not self.is_terminal_state and not self.is_archived

    @property
    def is_follow_up_overdue(self):
        if not self.follow_up_date or self.is_terminal_state:
            return False
        return self.follow_up_date < timezone.now().date()


class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='status_history')
    previous_status = models.CharField(max_length=50)
    new_status = models.CharField(max_length=50)
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.application.opportunity.company.name}: {self.previous_status} -> {self.new_status} on {self.changed_at.strftime('%Y-%m-%d')}"


class ApplicationNote(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='notes_log')
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note on {self.application} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
