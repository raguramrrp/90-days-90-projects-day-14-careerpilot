import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from .models import Reminder
from .forms import ReminderForm


@login_required
def reminder_list(request):
    today = timezone.now().date()
    tab = request.GET.get('tab', 'upcoming')
    reminders = Reminder.objects.filter(user=request.user).select_related('application', 'opportunity')

    if tab == 'overdue':
        reminders = reminders.filter(is_completed=False, due_date__lt=today).order_by('due_date')
    elif tab == 'today':
        reminders = reminders.filter(is_completed=False, due_date=today).order_by('due_time', 'priority')
    elif tab == 'upcoming':
        reminders = reminders.filter(is_completed=False, due_date__gte=today).order_by('due_date', 'due_time')
    elif tab == 'completed':
        reminders = reminders.filter(is_completed=True).order_by('-completed_at')
    else:  # all
        reminders = reminders.order_by('is_completed', 'due_date', 'due_time')

    # Filters
    reminder_type = request.GET.get('type')
    if reminder_type:
        reminders = reminders.filter(reminder_type=reminder_type)

    priority = request.GET.get('priority')
    if priority:
        reminders = reminders.filter(priority=priority)

    # Counts for tab badges
    counts = {
        'overdue': Reminder.objects.filter(user=request.user, is_completed=False, due_date__lt=today).count(),
        'today': Reminder.objects.filter(user=request.user, is_completed=False, due_date=today).count(),
        'upcoming': Reminder.objects.filter(user=request.user, is_completed=False, due_date__gte=today).count(),
        'completed': Reminder.objects.filter(user=request.user, is_completed=True).count(),
        'all': Reminder.objects.filter(user=request.user).count(),
    }

    return render(request, 'reminders/list.html', {
        'reminders': reminders,
        'tab': tab,
        'counts': counts,
        'types': Reminder.TYPE_CHOICES,
        'priorities': Reminder.PRIORITY_CHOICES,
        'current_type': reminder_type,
        'current_priority': priority,
    })


@login_required
def reminder_create(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST, user=request.user)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, f"Reminder '{reminder.title}' set for {reminder.due_date}.")
            return redirect('reminders:list')
        else:
            messages.error(request, "Please fix the form errors.")
    else:
        form = ReminderForm(user=request.user)

    return render(request, 'reminders/form.html', {
        'form': form,
        'title': 'Create New Reminder'
    })


@login_required
def reminder_update(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Reminder updated.")
            return redirect('reminders:list')
        else:
            messages.error(request, "Please fix the form errors.")
    else:
        form = ReminderForm(instance=reminder, user=request.user)

    return render(request, 'reminders/form.html', {
        'form': form,
        'reminder': reminder,
        'title': f"Edit Reminder: {reminder.title}"
    })


@login_required
def reminder_delete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == 'POST':
        title = reminder.title
        reminder.delete()
        messages.success(request, f"Reminder '{title}' deleted.")
        return redirect('reminders:list')

    return render(request, 'reminders/confirm_delete.html', {'reminder': reminder})


@login_required
def toggle_reminder_api(request, pk):
    """AJAX endpoint to mark reminder completed or incomplete."""
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")

    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)
        completed = data.get('completed', not reminder.is_completed)
    except Exception:
        completed = not reminder.is_completed

    if completed:
        reminder.mark_completed()
    else:
        reminder.mark_incomplete()

    return JsonResponse({
        'success': True,
        'is_completed': reminder.is_completed,
        'completed_at': reminder.completed_at.strftime('%Y-%m-%d %H:%M') if reminder.completed_at else None
    })
