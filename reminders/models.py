from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from applications.models import Application
from opportunities.models import Opportunity


class Reminder(models.Model):
    TYPE_CHOICES = [
        ('Application follow-up', 'Application Follow-up'),
        ('Interview reminder', 'Interview Reminder'),
        ('Assessment deadline', 'Assessment Deadline'),
        ('Job application deadline', 'Job Application Deadline'),
        ('Recruiter follow-up', 'Recruiter Follow-up'),
        ('Document submission', 'Document Submission'),
        ('Custom reminder', 'Custom Reminder'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reminder_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Application follow-up')
    
    application = models.ForeignKey(
        Application, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='reminders'
    )
    opportunity = models.ForeignKey(
        Opportunity, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='reminders'
    )
    
    due_date = models.DateField()
    due_time = models.TimeField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_completed', 'due_date', 'due_time', '-created_at']

    def __str__(self):
        status = "Completed" if self.is_completed else "Pending"
        return f"{self.title} ({self.due_date}) [{status}]"

    def mark_completed(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save(update_fields=['is_completed', 'completed_at', 'updated_at'])

    def mark_incomplete(self):
        self.is_completed = False
        self.completed_at = None
        self.save(update_fields=['is_completed', 'completed_at', 'updated_at'])

    @property
    def is_overdue(self):
        if self.is_completed or not self.due_date:
            return False
        return self.due_date < timezone.now().date()

    @property
    def is_due_today(self):
        if self.is_completed or not self.due_date:
            return False
        return self.due_date == timezone.now().date()
