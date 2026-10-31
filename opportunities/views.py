from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Opportunity, Company
from .forms import OpportunityForm


@login_required
def opportunity_list(request):
    queryset = Opportunity.objects.filter(user=request.user)

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(company__name__icontains=q) |
            Q(location__icontains=q) |
            Q(required_skills__icontains=q)
        )

    # Filters
    category = request.GET.get('category')
    if category:
        queryset = queryset.filter(category=category)

    employment_type = request.GET.get('employment_type')
    if employment_type:
        queryset = queryset.filter(employment_type=employment_type)

    work_mode = request.GET.get('work_mode')
    if work_mode:
        queryset = queryset.filter(work_mode=work_mode)

    source = request.GET.get('source')
    if source:
        queryset = queryset.filter(source=source)

    priority = request.GET.get('priority')
    if priority:
        queryset = queryset.filter(priority=priority)

    interest_status = request.GET.get('interest_status')
    if interest_status:
        queryset = queryset.filter(interest_status=interest_status)

    # Sorting
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = {
        'created_desc': '-created_at',
        'created_asc': 'created_at',
        'deadline_asc': 'deadline',
        'deadline_desc': '-deadline',
        'priority': 'priority',
        'title': 'title',
        'company': 'company__name'
    }
    order_by = valid_sorts.get(sort, '-created_at')
    queryset = queryset.order_by(order_by)

    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Opportunity.CATEGORY_CHOICES
    sources = Opportunity.SOURCE_CHOICES
    priorities = Opportunity.PRIORITY_CHOICES

    return render(request, 'opportunities/list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'sources': sources,
        'priorities': priorities,
        'current_q': q,
        'current_category': category,
        'current_employment_type': employment_type,
        'current_source': source,
        'current_priority': priority,
        'current_status': interest_status,
        'current_sort': sort,
        'is_saved_view': False
    })


@login_required
def saved_jobs_list(request):
    queryset = Opportunity.objects.filter(user=request.user, interest_status='Saved').order_by('-created_at')
    
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(company__name__icontains=q) |
            Q(required_skills__icontains=q)
        )

    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'opportunities/list.html', {
        'page_obj': page_obj,
        'is_saved_view': True,
        'current_q': q
    })


@login_required
def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, user=request.user)
    # Check if an application already exists for this opportunity
    existing_application = opportunity.applications.filter(is_archived=False).first()
    return render(request, 'opportunities/detail.html', {
        'opportunity': opportunity,
        'existing_application': existing_application
    })


@login_required
def opportunity_create(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST, user=request.user)
        if form.is_valid():
            company_name = form.cleaned_data.get('company_name').strip()
            company_website = form.cleaned_data.get('company_website')
            company = Company.objects.filter(user=request.user, name__iexact=company_name).first()
            if not company:
                company = Company.objects.create(
                    user=request.user,
                    name=company_name,
                    website=company_website or ''
                )
            elif company_website and not company.website:
                company.website = company_website
                company.save(update_fields=['website'])

            opp = form.save(commit=False)
            opp.user = request.user
            opp.company = company
            opp.save()
            messages.success(request, f"Opportunity '{opp.title}' at {company.name} was saved successfully.")
            return redirect('opportunities:detail', pk=opp.pk)
        else:
            messages.error(request, "Please fix the validation errors below.")
    else:
        form = OpportunityForm(user=request.user)

    return render(request, 'opportunities/form.html', {
        'form': form,
        'title': 'Add New Opportunity'
    })


@login_required
def opportunity_update(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, user=request.user)
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity, user=request.user)
        if form.is_valid():
            company_name = form.cleaned_data.get('company_name').strip()
            company_website = form.cleaned_data.get('company_website')
            company = Company.objects.filter(user=request.user, name__iexact=company_name).first()
            if not company:
                company = Company.objects.create(
                    user=request.user,
                    name=company_name,
                    website=company_website or ''
                )
            elif company_website and not company.website:
                company.website = company_website
                company.save(update_fields=['website'])

            opp = form.save(commit=False)
            opp.company = company
            opp.save()
            messages.success(request, f"Opportunity '{opp.title}' updated successfully.")
            return redirect('opportunities:detail', pk=opp.pk)
        else:
            messages.error(request, "Please fix the validation errors.")
    else:
        form = OpportunityForm(instance=opportunity, user=request.user)

    return render(request, 'opportunities/form.html', {
        'form': form,
        'opportunity': opportunity,
        'title': f"Edit Opportunity: {opportunity.title}"
    })


@login_required
def opportunity_delete(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, user=request.user)
    if request.method == 'POST':
        title = opportunity.title
        company_name = opportunity.company.name
        opportunity.delete()
        messages.success(request, f"Opportunity '{title}' at {company_name} was removed.")
        return redirect('opportunities:list')

    return render(request, 'opportunities/confirm_delete.html', {'opportunity': opportunity})


@login_required
def opportunity_toggle_status(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, user=request.user)
    new_status = request.POST.get('status')
    if new_status in dict(Opportunity.INTEREST_STATUS_CHOICES):
        opportunity.interest_status = new_status
        opportunity.save(update_fields=['interest_status', 'updated_at'])
        messages.success(request, f"Opportunity marked as '{new_status}'.")
    return redirect(request.META.get('HTTP_REFERER', 'opportunities:list'))


@login_required
def check_duplicate_api(request):
    """Checks if an opportunity with similar title at the same company already exists."""
    company_name = request.GET.get('company', '').strip()
    title = request.GET.get('title', '').strip()
    
    if not company_name or not title:
        return JsonResponse({'duplicate': False})

    existing = Opportunity.objects.filter(
        user=request.user,
        company__name__iexact=company_name,
        title__iexact=title
    ).first()

    if existing:
        return JsonResponse({
            'duplicate': True,
            'existing_id': existing.id,
            'existing_title': existing.title,
            'company': existing.company.name,
            'created_at': existing.created_at.strftime('%Y-%m-%d')
        })
    return JsonResponse({'duplicate': False})
