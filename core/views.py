from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from opportunities.models import Opportunity
from applications.models import Application, ApplicationStatusHistory
from interviews.models import Interview
from reminders.models import Reminder
from documents.models import Document
from planner.models import CareerTask, CareerGoal
from analytics.services import calculate_kpis, get_analytics_charts_data
from analytics.recommendations import get_career_recommendations


@login_required
def overview(request):
    """Main desktop command center / workspace dashboard."""
    today = timezone.now().date()
    kpis = calculate_kpis(request.user)
    charts_data = get_analytics_charts_data(request.user)
    recommendations = get_career_recommendations(request.user)

    # Approaching deadlines (next 7 days)
    upcoming_deadlines = Opportunity.objects.filter(
        user=request.user,
        deadline__gte=today,
        deadline__lte=today + timedelta(days=7),
        is_accepting_applications=True
    ).order_by('deadline')[:5]

    # Today's tasks
    todays_tasks = CareerTask.objects.filter(
        user=request.user,
        due_date=today,
    ).order_by('is_completed', 'priority')

    # Upcoming interviews
    upcoming_interviews = Interview.objects.filter(
        user=request.user,
        interview_date__gte=today,
        outcome='Scheduled'
    ).select_related('application', 'application__opportunity', 'application__opportunity__company').order_by('interview_date', 'interview_time')[:4]

    # Recent activity
    recent_history = ApplicationStatusHistory.objects.filter(
        application__user=request.user
    ).select_related('application', 'application__opportunity', 'application__opportunity__company').order_by('-changed_at')[:6]

    # Goals
    weekly_goals = CareerGoal.objects.filter(
        user=request.user,
        period_start_date__lte=today,
        period_end_date__gte=today
    )

    return render(request, 'core/overview.html', {
        'kpis': kpis,
        'charts_data': charts_data,
        'recommendations': recommendations[:4],
        'upcoming_deadlines': upcoming_deadlines,
        'todays_tasks': todays_tasks,
        'upcoming_interviews': upcoming_interviews,
        'recent_history': recent_history,
        'weekly_goals': weekly_goals,
        'today': today,
    })


@login_required
def my_day(request):
    """Dedicated Daily Planner view."""
    today = timezone.now().date()

    # Tasks
    tasks_today = CareerTask.objects.filter(user=request.user, due_date=today).order_by('is_completed', 'priority')
    tasks_overdue = CareerTask.objects.filter(user=request.user, due_date__lt=today, is_completed=False).order_by('due_date')
    tasks_completed_today = CareerTask.objects.filter(
        user=request.user,
        is_completed=True,
        completed_at__date=today
    ).order_by('-completed_at')

    # Reminders due today
    reminders_today = Reminder.objects.filter(
        user=request.user,
        due_date=today,
        is_completed=False
    ).select_related('application', 'opportunity')

    # Follow-ups due
    followups_due = Application.objects.filter(
        user=request.user,
        follow_up_date__lte=today,
        is_archived=False
    ).exclude(status__in=['Accepted', 'Rejected', 'Withdrawn']).select_related('opportunity', 'opportunity__company')

    # Upcoming interviews today and tomorrow
    interviews_soon = Interview.objects.filter(
        user=request.user,
        interview_date__gte=today,
        interview_date__lte=today + timedelta(days=2),
        outcome='Scheduled'
    ).select_related('application', 'application__opportunity', 'application__opportunity__company').order_by('interview_date', 'interview_time')

    # Assessment deadlines
    assessments_due = Application.objects.filter(
        user=request.user,
        status='Assessment',
        is_archived=False
    ).select_related('opportunity', 'opportunity__company')

    # Saved opportunities needing review
    saved_opportunities = Opportunity.objects.filter(
        user=request.user,
        interest_status='Saved'
    ).exclude(applications__is_archived=False)[:5]

    # Daily goals
    daily_goals = CareerGoal.objects.filter(
        user=request.user,
        goal_type='Daily',
        period_start_date__lte=today,
        period_end_date__gte=today
    )

    return render(request, 'core/my_day.html', {
        'today': today,
        'tasks_today': tasks_today,
        'tasks_overdue': tasks_overdue,
        'tasks_completed_today': tasks_completed_today,
        'reminders_today': reminders_today,
        'followups_due': followups_due,
        'interviews_soon': interviews_soon,
        'assessments_due': assessments_due,
        'saved_opportunities': saved_opportunities,
        'daily_goals': daily_goals,
    })


@login_required
def calendar_view(request):
    """Interactive calendar interface."""
    return render(request, 'core/calendar.html', {
        'today': timezone.now().date(),
    })


@login_required
def calendar_events_api(request):
    """Returns all career events formatted for the calendar."""
    user = request.user
    events = []

    # 1. Opportunity deadlines
    opps = Opportunity.objects.filter(user=user, deadline__isnull=False)
    for opp in opps:
        events.append({
            'id': f"opp_{opp.id}",
            'title': f"Deadline: {opp.title} @ {opp.company.name}",
            'date': opp.deadline.strftime('%Y-%m-%d'),
            'type': 'deadline',
            'badge': 'Deadline',
            'url': f"/opportunities/{opp.id}/",
            'priority': opp.priority,
            'color': '#C74E58'  # Danger / Red
        })

    # 2. Interviews
    interviews = Interview.objects.filter(user=user).select_related('application', 'application__opportunity', 'application__opportunity__company')
    for intv in interviews:
        time_str = f" at {intv.interview_time.strftime('%H:%M')}" if intv.interview_time else ""
        events.append({
            'id': f"int_{intv.id}",
            'title': f"Interview: {intv.application.opportunity.company.name} ({intv.round_title}){time_str}",
            'date': intv.interview_date.strftime('%Y-%m-%d'),
            'type': 'interview',
            'badge': 'Interview',
            'url': f"/interviews/{intv.id}/",
            'outcome': intv.outcome,
            'color': '#2869C7'  # Primary Accent / Blue
        })

    # 3. Reminders & Follow-ups
    reminders = Reminder.objects.filter(user=user)
    for rem in reminders:
        color = '#16856B' if rem.is_completed else ('#C58A25' if rem.is_overdue else '#66758A')
        events.append({
            'id': f"rem_{rem.id}",
            'title': f"Reminder: {rem.title}",
            'date': rem.due_date.strftime('%Y-%m-%d'),
            'type': 'reminder',
            'badge': rem.reminder_type,
            'url': f"/reminders/?tab={'completed' if rem.is_completed else 'all'}",
            'is_completed': rem.is_completed,
            'color': color
        })

    # 4. Career Tasks
    tasks = CareerTask.objects.filter(user=user)
    for t in tasks:
        events.append({
            'id': f"task_{t.id}",
            'title': f"Task: {t.title}",
            'date': t.due_date.strftime('%Y-%m-%d'),
            'type': 'task',
            'badge': t.category,
            'url': "/planner/",
            'is_completed': t.is_completed,
            'color': '#8B5CF6'  # Purple/Violet
        })

    return JsonResponse(events, safe=False)


@login_required
def global_search(request):
    """Global search across opportunities, applications, interviews, tasks, and documents."""
    q = request.GET.get('q', '').strip()
    results = {
        'opportunities': [],
        'applications': [],
        'interviews': [],
        'tasks': [],
        'documents': [],
    }

    if q:
        results['opportunities'] = Opportunity.objects.filter(
            user=request.user
        ).filter(
            title__icontains=q
        ) | Opportunity.objects.filter(
            user=request.user,
            company__name__icontains=q
        )

        results['applications'] = Application.objects.filter(
            user=request.user,
            is_archived=False
        ).filter(
            opportunity__title__icontains=q
        ) | Application.objects.filter(
            user=request.user,
            opportunity__company__name__icontains=q
        )

        results['interviews'] = Interview.objects.filter(
            user=request.user
        ).filter(
            round_title__icontains=q
        ) | Interview.objects.filter(
            user=request.user,
            application__opportunity__company__name__icontains=q
        )

        results['tasks'] = CareerTask.objects.filter(
            user=request.user,
            title__icontains=q
        )

        results['documents'] = Document.objects.filter(
            user=request.user,
            title__icontains=q
        )

    total_matches = (
        len(results['opportunities']) +
        len(results['applications']) +
        len(results['interviews']) +
        len(results['tasks']) +
        len(results['documents'])
    )

    return render(request, 'core/search.html', {
        'query': q,
        'results': results,
        'total_matches': total_matches,
    })


@login_required
def toggle_theme(request):
    """Toggles theme between Light and Dark mode."""
    if hasattr(request.user, 'profile'):
        current = request.user.profile.theme
        new_theme = 'dark' if current == 'light' else 'light'
        request.user.profile.theme = new_theme
        request.user.profile.save(update_fields=['theme'])
    else:
        new_theme = 'dark' if request.session.get('theme') == 'light' else 'light'
    
    request.session['theme'] = new_theme
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', ''):
        return JsonResponse({'success': True, 'theme': new_theme})

    return redirect(request.META.get('HTTP_REFERER', 'core:overview'))
