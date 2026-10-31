from django.utils import timezone


def careerpilot_context(request):
    if not request.user.is_authenticated:
        return {
            'notifications_count': 0,
            'user_theme': 'light',
            'today_date': timezone.now().date(),
        }

    from reminders.models import Reminder

    today = timezone.now().date()
    # Count overdue or due-today pending reminders
    overdue_or_today_reminders = Reminder.objects.filter(
        user=request.user,
        is_completed=False,
        due_date__lte=today
    ).count()

    theme = 'light'
    if hasattr(request.user, 'profile') and request.user.profile.theme:
        theme = request.user.profile.theme
    elif 'theme' in request.session:
        theme = request.session['theme']

    return {
        'notifications_count': overdue_or_today_reminders,
        'user_theme': theme,
        'today_date': today,
    }
