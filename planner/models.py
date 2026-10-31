from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from opportunities.models import Opportunity
from applications.models import Application


class CareerTask(models.Model):
    CATEGORY_CHOICES = [
        ('Job Search', 'Job Search & Discovery'),
        ('Application', 'Application Submission'),
        ('Interview Preparation', 'Interview Preparation'),
        ('Follow-up', 'Recruiter Follow-up'),
        ('Skill Development', 'Skill Development & Coding'),
        ('Resume Improvement', 'Resume & Document Polish'),
        ('Other', 'Other Task'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='career_tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Job Search')
    
    related_opportunity = models.ForeignKey(
        Opportunity,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tasks'
    )
    related_application = models.ForeignKey(
        Application,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tasks'
    )
    
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    due_date = models.DateField(default=timezone.now)
    due_time = models.TimeField(null=True, blank=True)
    
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_completed', 'due_date', 'due_time', '-created_at']

    def __str__(self):
        status = "Done" if self.is_completed else "Pending"
        return f"[{status}] {self.title} ({self.due_date})"

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


class CareerGoal(models.Model):
    GOAL_TYPES = [
        ('Daily', 'Daily Goal'),
        ('Weekly', 'Weekly Goal'),
    ]

    CATEGORY_CHOICES = [
        ('Applications', 'Applications Submitted'),
        ('Interview Prep', 'Interview Prep Sessions / Rounds'),
        ('Learning', 'Coding Problems / Technical Skills'),
        ('Outreach', 'Opportunities Reviewed / Saved'),
        ('Tasks', 'General Career Tasks Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='career_goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES, default='Weekly')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Applications')
    title = models.CharField(max_length=200)
    target_count = models.PositiveIntegerField(default=5)
    period_start_date = models.DateField(default=timezone.now)
    period_end_date = models.DateField()
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-period_end_date', 'goal_type']

    def __str__(self):
        return f"{self.goal_type}: {self.title} (Target: {self.target_count})"

    def calculate_current_progress(self):
        """Calculates actual progress based on real database records within the period."""
        from applications.models import Application
        from interviews.models import Interview
        from opportunities.models import Opportunity

        start = self.period_start_date
        end = self.period_end_date

        if self.category == 'Applications':
            return Application.objects.filter(
                user=self.user,
                application_date__gte=start,
                application_date__lte=end
            ).count()
        elif self.category == 'Interview Prep':
            # Count interviews or completed prep items
            return Interview.objects.filter(
                user=self.user,
                interview_date__gte=start,
                interview_date__lte=end
            ).count()
        elif self.category == 'Learning':
            # Count completed skill development tasks
            return CareerTask.objects.filter(
                user=self.user,
                category='Skill Development',
                is_completed=True,
                completed_at__date__gte=start,
                completed_at__date__lte=end
            ).count()
        elif self.category == 'Outreach':
            return Opportunity.objects.filter(
                user=self.user,
                created_at__date__gte=start,
                created_at__date__lte=end
            ).count()
        else:
            return CareerTask.objects.filter(
                user=self.user,
                is_completed=True,
                completed_at__date__gte=start,
                completed_at__date__lte=end
            ).count()

    @property
    def current_progress(self):
        return self.calculate_current_progress()

    @property
    def progress_percentage(self):
        if self.target_count <= 0:
            return 100
        prog = self.current_progress
        return min(100, int((prog / self.target_count) * 100))

    @property
    def is_achieved(self):
        return self.current_progress >= self.target_count
