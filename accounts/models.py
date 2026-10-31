from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    headline = models.CharField(max_length=200, blank=True, help_text="e.g. Aspiring AI/ML Engineer | B.Tech Student")
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=150, blank=True)
    
    preferred_roles = models.CharField(max_length=255, blank=True, help_text="Comma-separated job roles of interest")
    preferred_locations = models.CharField(max_length=255, blank=True, help_text="Preferred cities or Remote")
    preferred_employment_types = models.CharField(max_length=100, blank=True, default='Full-time')
    preferred_work_modes = models.CharField(max_length=100, blank=True, default='Hybrid')
    expected_salary = models.CharField(max_length=100, blank=True, help_text="e.g. 8-12 LPA or $80,000/yr")
    preferred_industries = models.CharField(max_length=255, blank=True)
    
    skill_profile = models.TextField(blank=True, help_text="Comma-separated skills (e.g. Python, Django, PostgreSQL, Scikit-Learn)")
    career_goals = models.TextField(blank=True, help_text="Immediate and 1-year career objectives")
    
    follow_up_default_days = models.PositiveIntegerField(default=7, help_text="Default days after applying to send recruiter follow-up")
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def skills_list(self):
        if not self.skill_profile:
            return []
        return [s.strip() for s in self.skill_profile.split(',') if s.strip()]


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            UserProfile.objects.create(user=instance)
