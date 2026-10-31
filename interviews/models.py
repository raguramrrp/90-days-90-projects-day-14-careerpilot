from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from applications.models import Application


class Interview(models.Model):
    MODE_CHOICES = [
        ('Online', 'Online Video Call'),
        ('Offline', 'In-Person / On-site'),
        ('Telephone', 'Telephone Screening'),
    ]

    OUTCOME_CHOICES = [
        ('Scheduled', 'Scheduled / Upcoming'),
        ('Completed', 'Completed — Awaiting Result'),
        ('Passed', 'Passed / Advanced'),
        ('Failed', 'Did Not Clear'),
        ('Rescheduled', 'Rescheduled'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    round_number = models.PositiveIntegerField(default=1)
    round_title = models.CharField(max_length=200, default='Round 1: Technical Interview')
    interview_date = models.DateField()
    interview_time = models.TimeField(null=True, blank=True)
    mode = models.CharField(max_length=50, choices=MODE_CHOICES, default='Online')
    meeting_url = models.URLField(max_length=500, blank=True)
    location = models.CharField(max_length=255, blank=True)
    
    interviewer_names = models.CharField(max_length=255, blank=True)
    interviewer_titles = models.CharField(max_length=255, blank=True)
    
    # Preparation
    preparation_notes = models.TextField(blank=True)
    topics_to_prepare = models.TextField(blank=True, help_text="e.g. Data Structures, System Design, Projects")
    
    # Post-interview evaluation & experience review
    outcome = models.CharField(max_length=50, choices=OUTCOME_CHOICES, default='Scheduled')
    feedback = models.TextField(blank=True)
    questions_asked = models.TextField(blank=True, help_text="Actual technical or behavioral questions asked")
    topics_covered = models.TextField(blank=True)
    personal_answers = models.TextField(blank=True, help_text="Notes on how you answered and code approaches")
    areas_to_improve = models.TextField(blank=True, help_text="Concepts or topics to review based on this round")
    next_round_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['interview_date', 'interview_time']

    def __str__(self):
        return f"{self.application.opportunity.company.name} - Round {self.round_number}: {self.round_title} ({self.interview_date})"

    @property
    def is_upcoming(self):
        if not self.interview_date:
            return False
        return self.interview_date >= timezone.now().date() and self.outcome == 'Scheduled'

    @property
    def is_today(self):
        return self.interview_date == timezone.now().date()


class InterviewChecklistItem(models.Model):
    DEFAULT_ITEMS = [
        "Research company products and recent news",
        "Review job description and key requirements",
        "Prepare 2-minute professional self-introduction",
        "Revise core technical concepts and algorithms",
        "Review resume projects and architectural decisions",
        "Prepare 3 thoughtful questions for the interviewer",
        "Test audio, webcam, and internet connection",
        "Have copies of resume and portfolio ready",
    ]

    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='checklist_items')
    item_text = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        status = "Done" if self.is_completed else "Pending"
        return f"[{status}] {self.item_text}"
