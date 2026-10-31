from django.utils import timezone
from datetime import timedelta
from collections import defaultdict, Counter
from opportunities.models import Opportunity
from applications.models import Application
from interviews.models import Interview
from reminders.models import Reminder


def calculate_kpis(user, start_date=None, end_date=None):
    """Calculates all key performance indicators from real database records."""
    today = timezone.now().date()
    
    opp_qs = Opportunity.objects.filter(user=user)
    app_qs = Application.objects.filter(user=user, is_archived=False)
    int_qs = Interview.objects.filter(user=user)
    rem_qs = Reminder.objects.filter(user=user)

    if start_date:
        app_qs = app_qs.filter(application_date__gte=start_date)
        opp_qs = opp_qs.filter(created_at__date__gte=start_date)
        int_qs = int_qs.filter(interview_date__gte=start_date)
    if end_date:
        app_qs = app_qs.filter(application_date__lte=end_date)
        opp_qs = opp_qs.filter(created_at__date__lte=end_date)
        int_qs = int_qs.filter(interview_date__lte=end_date)

    total_opps = opp_qs.count()
    total_apps = app_qs.count()
    in_progress = app_qs.exclude(status__in=['Accepted', 'Rejected', 'Withdrawn']).count()
    
    upcoming_interviews = int_qs.filter(interview_date__gte=today, outcome='Scheduled').count()
    pending_assessments = app_qs.filter(status='Assessment').count()
    overdue_followups = rem_qs.filter(is_completed=False, due_date__lt=today).count()
    
    offers_received = app_qs.filter(status__in=['Offer Received', 'Accepted']).count()
    offers_accepted = app_qs.filter(status='Accepted').count()

    # Calculate honest conversion rates
    interview_stage_count = app_qs.filter(status__in=['Technical Interview', 'HR Interview', 'Offer Received', 'Accepted']).count()
    app_to_interview_rate = round((interview_stage_count / total_apps * 100), 1) if total_apps > 0 else 0.0
    interview_to_offer_rate = round((offers_received / interview_stage_count * 100), 1) if interview_stage_count > 0 else 0.0
    offer_conversion_rate = round((offers_received / total_apps * 100), 1) if total_apps > 0 else 0.0

    return {
        'total_opportunities': total_opps,
        'total_applications': total_apps,
        'in_progress': in_progress,
        'upcoming_interviews': upcoming_interviews,
        'pending_assessments': pending_assessments,
        'overdue_followups': overdue_followups,
        'offers_received': offers_received,
        'offers_accepted': offers_accepted,
        'app_to_interview_rate': app_to_interview_rate,
        'interview_to_offer_rate': interview_to_offer_rate,
        'offer_conversion_rate': offer_conversion_rate,
    }


def get_analytics_charts_data(user, start_date=None, end_date=None):
    """Prepares structured data for all 10 Chart.js charts."""
    app_qs = Application.objects.filter(user=user, is_archived=False).select_related('opportunity')
    int_qs = Interview.objects.filter(user=user)

    if start_date:
        app_qs = app_qs.filter(application_date__gte=start_date)
        int_qs = int_qs.filter(interview_date__gte=start_date)
    if end_date:
        app_qs = app_qs.filter(application_date__lte=end_date)
        int_qs = int_qs.filter(interview_date__lte=end_date)

    # 1. Applications by month (last 6 months)
    today = timezone.now().date()
    months_labels = []
    months_keys = []
    for i in range(5, -1, -1):
        m_date = today - timedelta(days=i * 30)
        key = m_date.strftime('%Y-%m')
        label = m_date.strftime('%b %Y')
        if key not in months_keys:
            months_keys.append(key)
            months_labels.append(label)

    apps_by_month = {k: 0 for k in months_keys}
    for app in app_qs:
        k = app.application_date.strftime('%Y-%m')
        if k in apps_by_month:
            apps_by_month[k] += 1

    chart_apps_by_month = {
        'labels': months_labels,
        'data': [apps_by_month[k] for k in months_keys]
    }

    # 2. Pipeline stage distribution
    stage_counts = Counter(app.status for app in app_qs)
    stage_order = [s[0] for s in Application.STATUS_CHOICES]
    chart_pipeline = {
        'labels': stage_order,
        'data': [stage_counts.get(s, 0) for s in stage_order]
    }

    # 3. Applications by Job Category
    cat_counts = Counter(app.opportunity.category for app in app_qs)
    chart_category = {
        'labels': list(cat_counts.keys()) or ['No Data'],
        'data': list(cat_counts.values()) or [0]
    }

    # 4. Applications by Employment Type
    type_counts = Counter(app.opportunity.employment_type for app in app_qs)
    chart_employment_type = {
        'labels': list(type_counts.keys()) or ['No Data'],
        'data': list(type_counts.values()) or [0]
    }

    # 5. Applications by Work Mode
    mode_counts = Counter(app.opportunity.work_mode for app in app_qs)
    chart_work_mode = {
        'labels': list(mode_counts.keys()) or ['No Data'],
        'data': list(mode_counts.values()) or [0]
    }

    # 6. Applications by Source
    source_counts = Counter(app.opportunity.source for app in app_qs)
    chart_source = {
        'labels': list(source_counts.keys()) or ['No Data'],
        'data': list(source_counts.values()) or [0]
    }

    # 7. Interview Outcomes
    outcome_counts = Counter(intv.outcome for intv in int_qs)
    chart_interview_outcomes = {
        'labels': list(outcome_counts.keys()) or ['Scheduled'],
        'data': list(outcome_counts.values()) or [0]
    }

    # 8. Activity trends: Applications vs Interviews
    interviews_by_month = {k: 0 for k in months_keys}
    for intv in int_qs:
        k = intv.interview_date.strftime('%Y-%m')
        if k in interviews_by_month:
            interviews_by_month[k] += 1

    chart_activity_trend = {
        'labels': months_labels,
        'applications': [apps_by_month[k] for k in months_keys],
        'interviews': [interviews_by_month[k] for k in months_keys],
    }

    # 9. Offer Conversion Funnel
    total = app_qs.count()
    assessments = app_qs.filter(status__in=['Assessment', 'Technical Interview', 'HR Interview', 'Offer Received', 'Accepted']).count()
    interviews = app_qs.filter(status__in=['Technical Interview', 'HR Interview', 'Offer Received', 'Accepted']).count()
    offers = app_qs.filter(status__in=['Offer Received', 'Accepted']).count()
    accepted = app_qs.filter(status='Accepted').count()

    chart_funnel = {
        'labels': ['Applications', 'Assessments', 'Interviews', 'Offers', 'Accepted'],
        'data': [total, assessments, interviews, offers, accepted]
    }

    # 10. Status Breakdown (Active vs Terminal)
    terminal = app_qs.filter(status__in=['Accepted', 'Rejected', 'Withdrawn']).count()
    active = total - terminal
    chart_status_health = {
        'labels': ['Active In Pipeline', 'Decided / Terminal'],
        'data': [active, terminal]
    }

    return {
        'apps_by_month': chart_apps_by_month,
        'pipeline_distribution': chart_pipeline,
        'category_distribution': chart_category,
        'employment_type_distribution': chart_employment_type,
        'work_mode_distribution': chart_work_mode,
        'source_distribution': chart_source,
        'interview_outcomes': chart_interview_outcomes,
        'activity_trend': chart_activity_trend,
        'funnel': chart_funnel,
        'status_health': chart_status_health,
    }


def get_analytics_insights(user):
    """Provides actionable, plain-language insights based on real records."""
    app_qs = Application.objects.filter(user=user, is_archived=False).select_related('opportunity')
    total = app_qs.count()

    if total == 0:
        return [
            "Start by adding opportunities or recording applications to generate personalized strategy insights."
        ]

    insights = []
    # Most applied category
    cat_counts = Counter(app.opportunity.category for app in app_qs)
    top_cat, top_cat_count = cat_counts.most_common(1)[0]
    cat_pct = round((top_cat_count / total) * 100)
    insights.append(f"Most frequently targeted job category is '{top_cat}' ({cat_pct}% of total applications).")

    # Most productive source
    source_counts = Counter(app.opportunity.source for app in app_qs)
    top_source, top_source_count = source_counts.most_common(1)[0]
    insights.append(f"Primary discovery source is '{top_source}' with {top_source_count} opportunities tracked.")

    # Awaiting responses
    applied_count = app_qs.filter(status='Applied').count()
    if applied_count > 0:
        insights.append(f"{applied_count} application(s) currently in 'Applied' stage awaiting recruiter review.")

    # Offers
    offers = app_qs.filter(status__in=['Offer Received', 'Accepted']).count()
    if offers > 0:
        insights.append(f"Achieved {offers} job offer(s) so far with an overall conversion rate of {round((offers/total)*100, 1)}%.")
    else:
        insights.append("Focus on technical preparation and tailored resumes to advance from assessment to interview stages.")

    return insights
