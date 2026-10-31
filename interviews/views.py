import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Interview, InterviewChecklistItem
from .forms import InterviewForm, InterviewChecklistItemForm
from applications.models import Application
from reminders.models import Reminder


@login_required
def interview_list(request):
    queryset = Interview.objects.filter(user=request.user).select_related('application', 'application__opportunity', 'application__opportunity__company')

    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(round_title__icontains=q) |
            Q(application__opportunity__company__name__icontains=q) |
            Q(application__opportunity__title__icontains=q) |
            Q(topics_to_prepare__icontains=q)
        )

    outcome = request.GET.get('outcome')
    if outcome:
        queryset = queryset.filter(outcome=outcome)

    mode = request.GET.get('mode')
    if mode:
        queryset = queryset.filter(mode=mode)

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'interviews/list.html', {
        'page_obj': page_obj,
        'outcomes': Interview.OUTCOME_CHOICES,
        'modes': Interview.MODE_CHOICES,
        'current_q': q,
        'current_outcome': outcome,
        'current_mode': mode,
    })


@login_required
def interview_detail(request, pk):
    interview = get_object_or_404(
        Interview.objects.select_related('application', 'application__opportunity', 'application__opportunity__company'),
        pk=pk,
        user=request.user
    )
    checklist = interview.checklist_items.all()
    item_form = InterviewChecklistItemForm()

    return render(request, 'interviews/detail.html', {
        'interview': interview,
        'checklist': checklist,
        'item_form': item_form,
    })


@login_required
def interview_create(request):
    initial_data = {}
    app_id = request.GET.get('application_id')
    if app_id:
        app = get_object_or_404(Application, pk=app_id, user=request.user)
        initial_data['application'] = app
        initial_data['round_number'] = app.interviews.count() + 1
        initial_data['round_title'] = f"Round {initial_data['round_number']}: Technical Assessment"

    if request.method == 'POST':
        form = InterviewForm(request.POST, user=request.user)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.user = request.user
            interview.save()

            # Seed default preparation checklist items
            for item_text in InterviewChecklistItem.DEFAULT_ITEMS:
                InterviewChecklistItem.objects.create(
                    interview=interview,
                    item_text=item_text
                )

            # Create an interview reminder
            Reminder.objects.create(
                user=request.user,
                title=f"Interview: {interview.application.opportunity.company.name} - {interview.round_title}",
                description=f"Mode: {interview.mode}. Link: {interview.meeting_url or 'See details'}",
                reminder_type='Interview reminder',
                application=interview.application,
                opportunity=interview.application.opportunity,
                due_date=interview.interview_date,
                due_time=interview.interview_time,
                priority='High'
            )

            messages.success(request, f"Interview round scheduled for {interview.application.opportunity.company.name}!")
            return redirect('interviews:detail', pk=interview.pk)
        else:
            messages.error(request, "Please fix the validation errors below.")
    else:
        form = InterviewForm(initial=initial_data, user=request.user)

    return render(request, 'interviews/form.html', {
        'form': form,
        'title': 'Schedule Interview Round'
    })


@login_required
def interview_update(request, pk):
    interview = get_object_or_404(Interview, pk=pk, user=request.user)
    if request.method == 'POST':
        form = InterviewForm(request.POST, instance=interview, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Interview round details updated.")
            return redirect('interviews:detail', pk=interview.pk)
        else:
            messages.error(request, "Please fix the validation errors.")
    else:
        form = InterviewForm(instance=interview, user=request.user)

    return render(request, 'interviews/form.html', {
        'form': form,
        'interview': interview,
        'title': f"Edit Interview: {interview.round_title}"
    })


@login_required
def interview_delete(request, pk):
    interview = get_object_or_404(Interview, pk=pk, user=request.user)
    if request.method == 'POST':
        company_name = interview.application.opportunity.company.name
        round_title = interview.round_title
        interview.delete()
        messages.success(request, f"Interview '{round_title}' at {company_name} deleted.")
        return redirect('interviews:list')

    return render(request, 'interviews/confirm_delete.html', {'interview': interview})


@login_required
def toggle_checklist_api(request, item_id):
    """AJAX endpoint to toggle a checklist item's completion state."""
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")

    item = get_object_or_404(InterviewChecklistItem, pk=item_id, interview__user=request.user)
    try:
        data = json.loads(request.body)
        is_completed = data.get('completed', not item.is_completed)
    except Exception:
        is_completed = not item.is_completed

    item.is_completed = bool(is_completed)
    item.save(update_fields=['is_completed'])

    # Calculate overall progress of this interview's checklist
    total = item.interview.checklist_items.count()
    done = item.interview.checklist_items.filter(is_completed=True).count()
    percentage = int((done / total) * 100) if total > 0 else 0

    return JsonResponse({
        'success': True,
        'item_id': item.id,
        'is_completed': item.is_completed,
        'total_items': total,
        'completed_items': done,
        'percentage': percentage
    })


@login_required
def add_checklist_item(request, pk):
    interview = get_object_or_404(Interview, pk=pk, user=request.user)
    if request.method == 'POST':
        form = InterviewChecklistItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.interview = interview
            item.save()
            messages.success(request, "Checklist item added.")
        else:
            messages.error(request, "Checklist text cannot be empty.")
    return redirect('interviews:detail', pk=interview.pk)


@login_required
def preparation_notes_list(request):
    """Review past interview experiences, questions asked, and areas to improve."""
    interviews = Interview.objects.filter(
        user=request.user
    ).exclude(
        questions_asked='',
        topics_covered='',
        personal_answers='',
        areas_to_improve=''
    ).select_related('application', 'application__opportunity', 'application__opportunity__company')

    return render(request, 'interviews/preparation_notes.html', {
        'interviews': interviews,
    })
