import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
from .models import Application, ApplicationStatusHistory, ApplicationNote
from .forms import ApplicationForm, ApplicationNoteForm
from opportunities.models import Opportunity
from reminders.models import Reminder


@login_required
def application_list(request):
    queryset = Application.objects.filter(user=request.user, is_archived=False)

    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(opportunity__title__icontains=q) |
            Q(opportunity__company__name__icontains=q) |
            Q(recruiter_name__icontains=q) |
            Q(referral_name__icontains=q)
        )

    status = request.GET.get('status')
    if status:
        queryset = queryset.filter(status=status)

    method = request.GET.get('method')
    if method:
        queryset = queryset.filter(application_method=method)

    sort = request.GET.get('sort', '-application_date')
    valid_sorts = {
        'date_desc': '-application_date',
        'date_asc': 'application_date',
        'company': 'opportunity__company__name',
        'title': 'opportunity__title',
        'status': 'status',
    }
    order_by = valid_sorts.get(sort, '-application_date')
    queryset = queryset.order_by(order_by)

    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'applications/list.html', {
        'page_obj': page_obj,
        'statuses': Application.STATUS_CHOICES,
        'methods': Application.METHOD_CHOICES,
        'current_q': q,
        'current_status': status,
        'current_method': method,
        'current_sort': sort,
    })


@login_required
def application_kanban(request):
    """Interactive Kanban pipeline board grouped by the 10 stages."""
    apps = Application.objects.filter(user=request.user, is_archived=False).select_related('opportunity', 'opportunity__company', 'submitted_resume')
    
    stages = [
        ('Saved', 'Saved', 'text-slate-600'),
        ('Interested', 'Interested', 'text-sky-600'),
        ('Applied', 'Applied', 'text-blue-600'),
        ('Assessment', 'Assessment', 'text-amber-600'),
        ('Technical Interview', 'Tech Interview', 'text-indigo-600'),
        ('HR Interview', 'HR Interview', 'text-purple-600'),
        ('Offer Received', 'Offer Received', 'text-emerald-600'),
        ('Accepted', 'Accepted', 'text-green-700'),
        ('Rejected', 'Rejected', 'text-rose-600'),
        ('Withdrawn', 'Withdrawn', 'text-zinc-500'),
    ]

    columns = []
    for stage_key, stage_label, color_class in stages:
        stage_apps = [a for a in apps if a.status == stage_key]
        columns.append({
            'key': stage_key,
            'label': stage_label,
            'color_class': color_class,
            'count': len(stage_apps),
            'applications': stage_apps,
        })

    return render(request, 'applications/kanban.html', {
        'columns': columns,
        'total_active': len(apps),
    })


@login_required
def application_detail(request, pk):
    application = get_object_or_404(
        Application.objects.select_related('opportunity', 'opportunity__company', 'submitted_resume'),
        pk=pk,
        user=request.user
    )
    status_history = application.status_history.all()
    interviews = application.interviews.all()
    reminders = application.reminders.all()
    notes = application.notes_log.all()
    note_form = ApplicationNoteForm()

    return render(request, 'applications/detail.html', {
        'application': application,
        'status_history': status_history,
        'interviews': interviews,
        'reminders': reminders,
        'notes': notes,
        'note_form': note_form,
        'status_choices': Application.STATUS_CHOICES,
    })


@login_required
def application_create(request):
    initial_data = {}
    opp_id = request.GET.get('opportunity_id')
    if opp_id:
        opp = get_object_or_404(Opportunity, pk=opp_id, user=request.user)
        # If an active application already exists, redirect cleanly to it
        existing_app = Application.objects.filter(user=request.user, opportunity=opp, is_archived=False).first()
        if existing_app:
            messages.info(
                request,
                f"An active application for '{opp.title}' at {opp.company.name} already exists. Redirected to its detail view."
            )
            return redirect('applications:detail', pk=existing_app.pk)

        initial_data['opportunity'] = opp
        initial_data['expected_salary'] = opp.salary_max or opp.salary_min

    if request.method == 'POST':
        form = ApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user

            # Extra safety guard against race condition or re-submission
            existing = Application.objects.filter(
                user=request.user,
                opportunity=app.opportunity,
                is_archived=False
            ).first()
            if existing:
                messages.warning(
                    request,
                    f"An active application for '{app.opportunity.title}' at {app.opportunity.company.name} already exists."
                )
                return redirect('applications:detail', pk=existing.pk)

            try:
                app.save()
            except IntegrityError:
                messages.warning(
                    request,
                    f"An application for '{app.opportunity.title}' already exists in your workspace."
                )
                return redirect('applications:list')

            # Record initial status in history
            ApplicationStatusHistory.objects.create(
                application=app,
                previous_status='None',
                new_status=app.status,
                notes="Application created in CareerPilot."
            )

            # Create follow-up reminder if follow-up date is provided
            if app.follow_up_date:
                Reminder.objects.create(
                    user=request.user,
                    title=f"Follow up with {app.opportunity.company.name} for {app.opportunity.title}",
                    description=f"Check application status or reach out to recruiter {app.recruiter_name or ''}.",
                    reminder_type='Application follow-up',
                    application=app,
                    opportunity=app.opportunity,
                    due_date=app.follow_up_date,
                    priority='Medium'
                )

            messages.success(request, f"Application for {app.opportunity.title} at {app.opportunity.company.name} tracked successfully!")
            return redirect('applications:detail', pk=app.pk)
        else:
            messages.error(request, "Please fix the validation errors below.")
    else:
        form = ApplicationForm(initial=initial_data, user=request.user)

    return render(request, 'applications/form.html', {
        'form': form,
        'title': 'Track New Application'
    })


@login_required
def application_update(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    prev_status = application.status

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application, user=request.user)
        if form.is_valid():
            try:
                app = form.save()
            except IntegrityError:
                messages.error(request, "An application for this opportunity already exists.")
                return render(request, 'applications/form.html', {
                    'form': form,
                    'application': application,
                    'title': f"Edit Application: {application.opportunity.title}"
                })

            # If status changed, record history
            if app.status != prev_status:
                ApplicationStatusHistory.objects.create(
                    application=app,
                    previous_status=prev_status,
                    new_status=app.status,
                    notes=f"Status changed from {prev_status} to {app.status} via edit form."
                )
            messages.success(request, "Application details updated.")
            return redirect('applications:detail', pk=app.pk)
        else:
            messages.error(request, "Please fix the validation errors.")
    else:
        form = ApplicationForm(instance=application, user=request.user)

    return render(request, 'applications/form.html', {
        'form': form,
        'application': application,
        'title': f"Edit Application: {application.opportunity.title}"
    })


@login_required
def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        company_name = application.opportunity.company.name
        title = application.opportunity.title
        application.delete()
        messages.success(request, f"Application for '{title}' at {company_name} deleted.")
        return redirect('applications:list')

    return render(request, 'applications/confirm_delete.html', {'application': application})


@login_required
def update_status_api(request, pk):
    """AJAX endpoint for Kanban board or quick status update."""
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")

    application = get_object_or_404(Application, pk=pk, user=request.user)
    
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        notes = data.get('notes', 'Status updated via pipeline board.')
    except Exception:
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', 'Status updated.')

    valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]
    if new_status not in valid_statuses:
        return JsonResponse({'success': False, 'error': 'Invalid status choice'}, status=400)

    if application.status != new_status:
        prev_status = application.status
        application.status = new_status
        application.save(update_fields=['status', 'updated_at'])
        
        # Save history
        history = ApplicationStatusHistory.objects.create(
            application=application,
            previous_status=prev_status,
            new_status=new_status,
            notes=notes
        )

        return JsonResponse({
            'success': True,
            'previous_status': prev_status,
            'new_status': new_status,
            'changed_at': history.changed_at.strftime('%Y-%m-%d %H:%M')
        })

    return JsonResponse({'success': True, 'unchanged': True})


@login_required
def add_note(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ApplicationNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.application = application
            note.save()
            messages.success(request, "Note added to application history.")
        else:
            messages.error(request, "Note cannot be empty.")
    return redirect('applications:detail', pk=application.pk)
