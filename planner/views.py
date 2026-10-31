import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from .models import CareerTask, CareerGoal
from .forms import CareerTaskForm, CareerGoalForm


@login_required
def task_list(request):
    today = timezone.now().date()
    status_filter = request.GET.get('status', 'all')
    tasks = CareerTask.objects.filter(user=request.user).select_related('related_opportunity', 'related_application')

    if status_filter == 'pending':
        tasks = tasks.filter(is_completed=False)
    elif status_filter == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif status_filter == 'today':
        tasks = tasks.filter(is_completed=False, due_date=today)
    elif status_filter == 'overdue':
        tasks = tasks.filter(is_completed=False, due_date__lt=today)

    category = request.GET.get('category')
    if category:
        tasks = tasks.filter(category=category)

    priority = request.GET.get('priority')
    if priority:
        tasks = tasks.filter(priority=priority)

    goals = CareerGoal.objects.filter(user=request.user)

    return render(request, 'planner/list.html', {
        'tasks': tasks,
        'goals': goals,
        'status_filter': status_filter,
        'categories': CareerTask.CATEGORY_CHOICES,
        'priorities': CareerTask.PRIORITY_CHOICES,
        'current_category': category,
        'current_priority': priority,
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        form = CareerTaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' added to your career planner.")
            return redirect(request.GET.get('next') or 'planner:task_list')
        else:
            messages.error(request, "Please fix the task errors below.")
    else:
        form = CareerTaskForm(user=request.user)

    return render(request, 'planner/task_form.html', {
        'form': form,
        'title': 'Add Career Task'
    })


@login_required
def task_update(request, pk):
    task = get_object_or_404(CareerTask, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CareerTaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated.")
            return redirect('planner:task_list')
        else:
            messages.error(request, "Please fix the task errors.")
    else:
        form = CareerTaskForm(instance=task, user=request.user)

    return render(request, 'planner/task_form.html', {
        'form': form,
        'task': task,
        'title': f"Edit Task: {task.title}"
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(CareerTask, pk=pk, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f"Task '{title}' deleted.")
        return redirect('planner:task_list')

    return render(request, 'planner/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle_api(request, pk):
    """AJAX endpoint to complete or uncomplete a career task."""
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")

    task = get_object_or_404(CareerTask, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)
        completed = data.get('completed', not task.is_completed)
    except Exception:
        completed = not task.is_completed

    if completed:
        task.mark_completed()
    else:
        task.mark_incomplete()

    return JsonResponse({
        'success': True,
        'is_completed': task.is_completed,
        'completed_at': task.completed_at.strftime('%Y-%m-%d %H:%M') if task.completed_at else None
    })


@login_required
def goal_create(request):
    if request.method == 'POST':
        form = CareerGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f"Goal '{goal.title}' created.")
            return redirect('planner:task_list')
        else:
            messages.error(request, "Please fix goal errors.")
    else:
        form = CareerGoalForm()

    return render(request, 'planner/goal_form.html', {
        'form': form,
        'title': 'Create Career Goal'
    })


@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(CareerGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        title = goal.title
        goal.delete()
        messages.success(request, f"Goal '{title}' deleted.")
        return redirect('planner:task_list')

    return render(request, 'planner/goal_confirm_delete.html', {'goal': goal})
