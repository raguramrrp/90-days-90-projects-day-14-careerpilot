from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from .services import calculate_kpis, get_analytics_charts_data, get_analytics_insights
from .recommendations import get_career_recommendations


@login_required
def analytics_dashboard(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = None
    end_date = None
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass

    kpis = calculate_kpis(request.user, start_date=start_date, end_date=end_date)
    charts_data = get_analytics_charts_data(request.user, start_date=start_date, end_date=end_date)
    insights = get_analytics_insights(request.user)
    recommendations = get_career_recommendations(request.user)

    return render(request, 'analytics/dashboard.html', {
        'kpis': kpis,
        'charts_data': charts_data,
        'insights': insights,
        'recommendations': recommendations,
        'start_date': start_date_str or '',
        'end_date': end_date_str or '',
    })


@login_required
def chart_data_api(request):
    charts_data = get_analytics_charts_data(request.user)
    return JsonResponse(charts_data)
