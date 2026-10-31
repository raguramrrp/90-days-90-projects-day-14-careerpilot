from django.utils import timezone
from datetime import timedelta
from opportunities.models import Opportunity
from applications.models import Application
from interviews.models import Interview
from reminders.models import Reminder


def get_career_recommendations(user):
    """
    Evaluates real database records to produce prioritized, rule-based recommendations.
    Never fabricates or generates random suggestions.
    """
    today = timezone.now().date()
    recs = []

    # 1. Check for upcoming opportunities deadlines (within next 3 days)
    approaching_deadlines = Opportunity.objects.filter(
        user=user,
        deadline__gte=today,
        deadline__lte=today + timedelta(days=3),
        is_accepting_applications=True
    ).exclude(applications__is_archived=False)

    for opp in approaching_deadlines:
        days_left = (opp.deadline - today).days
        recs.append({
            'title': f"Application Deadline Approaching: {opp.title}",
            'reason': f"Deadline is in {days_left} day(s) ({opp.deadline}) for {opp.company.name}.",
            'priority': 'Urgent' if days_left <= 1 else 'High',
            'suggested_action': "Submit application and record details before the portal closes.",
            'action_url': f"/opportunities/{opp.id}/",
            'badge': 'Deadline'
        })

    # 2. Check for interview scheduled today or tomorrow
    upcoming_interviews = Interview.objects.filter(
        user=user,
        interview_date__gte=today,
        interview_date__lte=today + timedelta(days=1),
        outcome='Scheduled'
    ).select_related('application', 'application__opportunity', 'application__opportunity__company')

    for interview in upcoming_interviews:
        when = "TODAY" if interview.interview_date == today else "TOMORROW"
        recs.append({
            'title': f"Interview {when}: {interview.application.opportunity.company.name}",
            'reason': f"{interview.round_title} scheduled for {interview.interview_date} ({interview.interview_time or 'Time TBD'}).",
            'priority': 'Urgent',
            'suggested_action': "Review checklist, check equipment, and review company questions.",
            'action_url': f"/interviews/{interview.id}/",
            'badge': 'Interview'
        })

    # 3. Check for overdue follow-ups
    overdue_apps = Application.objects.filter(
        user=user,
        is_archived=False,
        follow_up_date__lt=today,
    ).exclude(status__in=['Accepted', 'Rejected', 'Withdrawn']).select_related('opportunity', 'opportunity__company')

    for app in overdue_apps[:3]:
        days_over = (today - app.follow_up_date).days
        recs.append({
            'title': f"Follow-up Overdue: {app.opportunity.company.name}",
            'reason': f"Follow-up target date was {app.follow_up_date} ({days_over} days overdue).",
            'priority': 'High',
            'suggested_action': f"Send a polite inquiry email to {app.recruiter_name or 'the recruiter'}.",
            'action_url': f"/applications/{app.id}/",
            'badge': 'Follow-up'
        })

    # 4. Check for multiple interviews on the same day
    interview_dates = Interview.objects.filter(
        user=user,
        interview_date__gte=today,
        outcome='Scheduled'
    ).values_list('interview_date', flat=True)

    from collections import Counter
    date_counts = Counter(interview_dates)
    for date_val, count in date_counts.items():
        if count > 1:
            recs.append({
                'title': f"Schedule Conflict Alert: {count} interviews on {date_val}",
                'reason': f"You have {count} rounds scheduled on the same date. Ensure sufficient rest and spacing.",
                'priority': 'High',
                'suggested_action': "Review round timings to ensure no overlaps.",
                'action_url': "/interviews/",
                'badge': 'Schedule'
            })

    # 5. Check if application has remained unanswered beyond default follow-up period
    default_days = getattr(user.profile, 'follow_up_default_days', 7) or 7
    stale_threshold = today - timedelta(days=default_days + 3)
    stale_apps = Application.objects.filter(
        user=user,
        status='Applied',
        application_date__lte=stale_threshold,
        is_archived=False
    ).select_related('opportunity', 'opportunity__company')

    for app in stale_apps[:2]:
        recs.append({
            'title': f"No Response Received: {app.opportunity.company.name}",
            'reason': f"Applied on {app.application_date} with no pipeline movement.",
            'priority': 'Medium',
            'suggested_action': "Check recruiter LinkedIn or consider follow-up reminder.",
            'action_url': f"/applications/{app.id}/",
            'badge': 'Stale Pipeline'
        })

    # 6. Check for saved opportunities matching user preferred role
    if hasattr(user, 'profile') and user.profile.preferred_roles:
        roles = [r.strip().lower() for r in user.profile.preferred_roles.split(',') if r.strip()]
        for role in roles:
            matching_saved = Opportunity.objects.filter(
                user=user,
                interest_status='Saved',
                title__icontains=role
            ).exclude(applications__is_archived=False)[:1]
            for m in matching_saved:
                recs.append({
                    'title': f"Opportunity Matches Preferred Role: {m.title}",
                    'reason': f"Matches your target role '{role}' at {m.company.name}.",
                    'priority': 'Medium',
                    'suggested_action': "Review job description and start application.",
                    'action_url': f"/opportunities/{m.id}/",
                    'badge': 'Role Match'
                })

    # Sort recommendations by priority (Urgent -> High -> Medium)
    priority_order = {'Urgent': 0, 'High': 1, 'Medium': 2, 'Low': 3}
    recs.sort(key=lambda r: priority_order.get(r['priority'], 4))
    return recs
