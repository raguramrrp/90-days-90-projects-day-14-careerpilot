import io
import csv
from datetime import datetime
import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from applications.models import Application
from opportunities.models import Opportunity
from interviews.models import Interview
from planner.models import CareerTask


@login_required
def report_center(request):
    total_apps = Application.objects.filter(user=request.user).count()
    total_opps = Opportunity.objects.filter(user=request.user).count()
    total_ints = Interview.objects.filter(user=request.user).count()
    total_tasks = CareerTask.objects.filter(user=request.user).count()

    return render(request, 'reports/export.html', {
        'total_apps': total_apps,
        'total_opps': total_opps,
        'total_ints': total_ints,
        'total_tasks': total_tasks,
    })


@login_required
def export_applications_csv(request):
    apps = Application.objects.filter(user=request.user, is_archived=False).select_related('opportunity', 'opportunity__company')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="careerpilot_applications.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Application ID', 'Company', 'Job Title', 'Category', 'Employment Type',
        'Work Mode', 'Location', 'Status', 'Application Date', 'Method',
        'Follow-up Date', 'Expected Salary', 'Offered Salary', 'Recruiter Name',
        'Recruiter Email', 'Referral', 'Notes'
    ])

    for a in apps:
        writer.writerow([
            a.id,
            a.opportunity.company.name,
            a.opportunity.title,
            a.opportunity.category,
            a.opportunity.employment_type,
            a.opportunity.work_mode,
            a.opportunity.location,
            a.status,
            a.application_date.strftime('%Y-%m-%d') if a.application_date else '',
            a.application_method,
            a.follow_up_date.strftime('%Y-%m-%d') if a.follow_up_date else '',
            a.expected_salary or '',
            a.offered_salary or '',
            a.recruiter_name or '',
            a.recruiter_email or '',
            a.referral_name or '',
            a.notes or ''
        ])

    return response


@login_required
def export_applications_excel(request):
    apps = Application.objects.filter(user=request.user, is_archived=False).select_related('opportunity', 'opportunity__company')

    data = []
    for a in apps:
        data.append({
            'ID': a.id,
            'Company': a.opportunity.company.name,
            'Title': a.opportunity.title,
            'Category': a.opportunity.category,
            'Employment Type': a.opportunity.employment_type,
            'Work Mode': a.opportunity.work_mode,
            'Location': a.opportunity.location,
            'Status': a.status,
            'Applied Date': a.application_date.strftime('%Y-%m-%d') if a.application_date else '',
            'Method': a.application_method,
            'Follow-up Date': a.follow_up_date.strftime('%Y-%m-%d') if a.follow_up_date else '',
            'Expected Salary': float(a.expected_salary) if a.expected_salary else None,
            'Offered Salary': float(a.offered_salary) if a.offered_salary else None,
            'Recruiter': a.recruiter_name,
            'Recruiter Email': a.recruiter_email,
            'Referral': a.referral_name,
            'Notes': a.notes,
        })

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Applications')

    output.seek(0)
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="careerpilot_applications.xlsx"'
    return response


@login_required
def export_opportunities_csv(request):
    opps = Opportunity.objects.filter(user=request.user).select_related('company')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="careerpilot_opportunities.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Company', 'Title', 'Category', 'Employment Type', 'Work Mode',
        'Location', 'Min Salary', 'Max Salary', 'Source', 'Application URL',
        'Deadline', 'Priority', 'Status', 'Date Added'
    ])

    for o in opps:
        writer.writerow([
            o.id,
            o.company.name,
            o.title,
            o.category,
            o.employment_type,
            o.work_mode,
            o.location,
            o.salary_min or '',
            o.salary_max or '',
            o.source,
            o.application_url or '',
            o.deadline.strftime('%Y-%m-%d') if o.deadline else '',
            o.priority,
            o.interest_status,
            o.created_at.strftime('%Y-%m-%d')
        ])

    return response


@login_required
def export_opportunities_excel(request):
    opps = Opportunity.objects.filter(user=request.user).select_related('company')

    data = []
    for o in opps:
        data.append({
            'ID': o.id,
            'Company': o.company.name,
            'Title': o.title,
            'Category': o.category,
            'Employment Type': o.employment_type,
            'Work Mode': o.work_mode,
            'Location': o.location,
            'Min Salary': float(o.salary_min) if o.salary_min else None,
            'Max Salary': float(o.salary_max) if o.salary_max else None,
            'Source': o.source,
            'Application URL': o.application_url,
            'Deadline': o.deadline.strftime('%Y-%m-%d') if o.deadline else '',
            'Priority': o.priority,
            'Status': o.interest_status,
            'Date Added': o.created_at.strftime('%Y-%m-%d'),
        })

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Opportunities')

    output.seek(0)
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="careerpilot_opportunities.xlsx"'
    return response


@login_required
def export_interviews_csv(request):
    ints = Interview.objects.filter(user=request.user).select_related('application', 'application__opportunity', 'application__opportunity__company')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="careerpilot_interviews.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Company', 'Job Title', 'Round', 'Title', 'Date', 'Time',
        'Mode', 'Outcome', 'Feedback', 'Questions Asked', 'Topics Covered', 'Areas to Improve'
    ])

    for i in ints:
        writer.writerow([
            i.id,
            i.application.opportunity.company.name,
            i.application.opportunity.title,
            i.round_number,
            i.round_title,
            i.interview_date.strftime('%Y-%m-%d') if i.interview_date else '',
            i.interview_time.strftime('%H:%M') if i.interview_time else '',
            i.mode,
            i.outcome,
            i.feedback or '',
            i.questions_asked or '',
            i.topics_covered or '',
            i.areas_to_improve or ''
        ])

    return response
